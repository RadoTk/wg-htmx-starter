from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, PublishingPanel
from wagtail.api import APIField
from wagtail.models import DraftStateMixin, PreviewableMixin, RevisionMixin, TranslatableMixin


class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):
    body = RichTextField()

    revisions = GenericRelation(
        "wagtailcore.Revision",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="footer_text",
        for_concrete_model=False,
    )

    panels = [FieldPanel("body"), PublishingPanel()]
    api_fields = [APIField("body")]

    def __str__(self):
        return "Footer text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name = "footer text"
        verbose_name_plural = "footer text"
