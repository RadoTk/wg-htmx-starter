from django import forms
from django.contrib.contenttypes.fields import GenericRelation
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import DraftStateMixin, Page, RevisionMixin
from wagtail.search import index

from rootapp.base.blocks import BaseStreamBlock


# -----------------------------------------------------------------------------
# PRODUCT DATA MODELS
# -----------------------------------------------------------------------------

class ProductOrigin(models.Model):
    """
    Represents a country or region of origin for a product.
    Used as a snippet in Wagtail admin via ProductOriginSnippetViewSet.
    """

    title = models.CharField(max_length=100)

    panels = [FieldPanel("title")]

    api_fields = [APIField("title")]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "product origin"
        verbose_name_plural = "product origins"


class ProductIngredient(DraftStateMixin, RevisionMixin, models.Model):
    """
    Represents a single ingredient used in products.
    Managed as a snippet in the Wagtail admin.
    """

    name = models.CharField(max_length=255)

    revisions = GenericRelation(
        "wagtailcore.Revision",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="product_ingredient",
        for_concrete_model=False,
    )

    panels = [FieldPanel("name")]

    api_fields = [APIField("name")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "product ingredient"
        verbose_name_plural = "product ingredients"


class ProductCategory(RevisionMixin, models.Model):
    """
    Represents a category or type of product.
    Managed as a snippet in the Wagtail admin.
    """

    title = models.CharField(max_length=255)

    revisions = GenericRelation(
        "wagtailcore.Revision",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="product_category",
        for_concrete_model=False,
    )

    panels = [FieldPanel("title")]

    api_fields = [APIField("title")]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "product category"
        verbose_name_plural = "product categories"


# -----------------------------------------------------------------------------
# PRODUCT ARTICLE PAGES
# -----------------------------------------------------------------------------

class ProductArticlePage(Page):
    """
    Represents an editorial or detailed content page about a product.
    Similar to a blog post or product story.
    """

    introduction = models.TextField(
        blank=True,
        help_text="Optional short description of this article or product page."
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape image only (1000px–3000px width)."
    )

    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Page body",
        blank=True,
        use_json_field=True,
    )

    origin = models.ForeignKey(
        "ProductOrigin",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Product origin",
    )

    category = models.ForeignKey(
        "ProductCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Product category",
    )

    ingredients = ParentalManyToManyField(
        "ProductIngredient",
        blank=True,
        verbose_name="Product ingredients",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("origin"),
                FieldPanel("category"),
                FieldPanel("ingredients", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Product details",
            classname="collapsed",
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]

    parent_page_types = ["ProductArticlesIndexPage"]
    subpage_types = []

    api_fields = [
        APIField("introduction"),
        APIField("image"),
        APIField("body"),
        APIField("origin"),
        APIField("category"),
        APIField("ingredients"),
    ]

    class Meta:
        verbose_name = "product article"
        verbose_name_plural = "product articles"


class ProductArticlesIndexPage(Page):
    """
    An index page listing ProductArticlePage entries with pagination.
    """

    introduction = models.TextField(
        blank=True,
        help_text="Text displayed at the top of the product articles index page."
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional header image for the index page.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
    ]

    subpage_types = ["ProductArticlePage"]

    api_fields = [
        APIField("introduction"),
        APIField("image"),
    ]

    class Meta:
        verbose_name = "product articles index"
        verbose_name_plural = "product articles indexes"

    # -------------------------------------------------------------------------
    # Query methods
    # -------------------------------------------------------------------------

    def get_articles(self):
        """Return live ProductArticlePages under this index, newest first."""
        return ProductArticlePage.objects.live().descendant_of(self).order_by("-first_published_at")

    def children(self):
        """Return all live children for Wagtail templates."""
        return self.get_children().specific().live()

    # -------------------------------------------------------------------------
    # Pagination
    # -------------------------------------------------------------------------

    def paginate(self, request, articles, per_page=12):
        page_number = request.GET.get("page")
        paginator = Paginator(articles, per_page)
        try:
            pages = paginator.page(page_number)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    # -------------------------------------------------------------------------
    # Context
    # -------------------------------------------------------------------------

    def get_context(self, request):
        context = super().get_context(request)
        articles = self.paginate(request, self.get_articles())
        context["articles"] = articles
        return context
