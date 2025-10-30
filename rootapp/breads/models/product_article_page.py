from django import forms
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.search import index
from modelcluster.fields import ParentalManyToManyField
from rootapp.base.blocks import BaseStreamBlock

from .product_origin import ProductOrigin
from .product_category import ProductCategory
from .product_ingredient import ProductIngredient

class ProductArticlePage(Page):
    introduction = models.TextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(BaseStreamBlock(), blank=True, use_json_field=True)
    origin = models.ForeignKey(ProductOrigin, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    ingredients = ParentalManyToManyField(ProductIngredient, blank=True)

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
