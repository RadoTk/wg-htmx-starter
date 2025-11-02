from django.db import models
from wagtail.models import Page, Collection
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import (
    FieldPanel, MultiFieldPanel, HelpPanel, FieldRowPanel
)
from wagtail.api import APIField
from rootapp.base.blocks import BaseStreamBlock


class StandardPage(Page):
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    body = StreamField(BaseStreamBlock(), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("image"),
    ]

    api_fields = [APIField("introduction"), APIField("image"), APIField("body")]


class HomePage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    hero_text = models.CharField(max_length=255)
    hero_cta = models.CharField(max_length=255)
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    body = StreamField(BaseStreamBlock(), blank=True, use_json_field=True)
    promo_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    promo_title = models.CharField(blank=True, max_length=255)
    promo_text = RichTextField(blank=True, max_length=1000)
    featured_section_1_title = models.CharField(blank=True, max_length=255)
    featured_section_1 = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    featured_section_2_title = models.CharField(blank=True, max_length=255)
    featured_section_2 = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    featured_section_3_title = models.CharField(blank=True, max_length=255)
    featured_section_3 = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_text"),
                FieldPanel("hero_cta"),
                FieldPanel("hero_cta_link"),
            ],
            heading="Hero section",
        ),
        HelpPanel("This is a help panel"),
        MultiFieldPanel(
            [
                FieldPanel("promo_image"),
                FieldPanel("promo_title"),
                FieldPanel("promo_text"),
            ],
            heading="Promo section",
        ),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("featured_section_1_title"),
                FieldPanel("featured_section_1"),
                FieldPanel("featured_section_2_title"),
                FieldPanel("featured_section_2"),
                FieldPanel("featured_section_3_title"),
                FieldPanel("featured_section_3"),
            ],
            heading="Featured homepage sections",
        ),
    ]

    api_fields = [
        APIField("image"),
        APIField("hero_text"),
        APIField("hero_cta"),
        APIField("hero_cta_link"),
        APIField("body"),
        APIField("promo_image"),
        APIField("promo_title"),
        APIField("promo_text"),
        APIField("featured_section_1_title"),
        APIField("featured_section_1"),
        APIField("featured_section_2_title"),
        APIField("featured_section_2"),
        APIField("featured_section_3_title"),
        APIField("featured_section_3"),
    ]

    def __str__(self):
        return self.title


class GalleryPage(Page):
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    body = StreamField(BaseStreamBlock(), blank=True, use_json_field=True)
    collection = models.ForeignKey(
        Collection, null=True, blank=True,
        on_delete=models.SET_NULL,
        help_text="Select the image collection for this gallery.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("collection"),
    ]

    subpage_types = []
    api_fields = [
        APIField("introduction"),
        APIField("image"),
        APIField("body"),
        APIField("collection"),
    ]
