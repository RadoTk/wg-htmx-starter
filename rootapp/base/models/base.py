from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext as _
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel, FieldRowPanel, MultiFieldPanel, PublishingPanel
)
from wagtail.api import APIField
from wagtail.models import (
    DraftStateMixin, LockableMixin, PreviewableMixin, RevisionMixin,
    WorkflowMixin
)
from wagtail.search import index

# Allow filtering by collection
from wagtail.images.models import Image
Image.api_fields = [APIField("collection")]


class Person(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    PreviewableMixin,
    index.Indexed,
    ClusterableModel,
):
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    job_title = models.CharField("Job title", max_length=254)

    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )

    workflow_states = GenericRelation(
        "wagtailcore.WorkflowState",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="person",
        for_concrete_model=False,
    )

    revisions = GenericRelation(
        "wagtailcore.Revision",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="person",
        for_concrete_model=False,
    )

    panels = [
        MultiFieldPanel(
            [FieldRowPanel([FieldPanel("first_name"), FieldPanel("last_name")])],
            "Name",
        ),
        FieldPanel("job_title"),
        FieldPanel("image"),
        PublishingPanel(),
    ]

    search_fields = [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
        index.FilterField("job_title"),
        index.AutocompleteField("first_name"),
        index.AutocompleteField("last_name"),
    ]

    api_fields = [
        APIField("first_name"),
        APIField("last_name"),
        APIField("job_title"),
        APIField("image"),
    ]

    @property
    def thumb_image(self):
        try:
            return self.image.get_rendition("fill-50x50").img_tag()
        except Exception:
            return ""

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + [("blog_post", _("Blog post"))]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_preview_template(self, request, mode_name):
        from rootapp.blog.models import BlogPage
        if mode_name == "blog_post":
            return BlogPage.template
        return "base/preview/person.html"

    def get_preview_context(self, request, mode_name):
        from rootapp.blog.models import BlogPage
        context = super().get_preview_context(request, mode_name)
        if mode_name == self.default_preview_mode:
            return context

        page = BlogPage.objects.filter(blog_person_relationship__person=self).first()
        if page:
            page.authors = [
                self if author.pk == self.pk else author for author in page.authors()
            ]
            if not self.live:
                page.authors.append(self)
        else:
            page = BlogPage.objects.first()
            page.authors = [self]

        context["page"] = page
        return context

    class Meta:
        verbose_name = "person"
        verbose_name_plural = "people"
