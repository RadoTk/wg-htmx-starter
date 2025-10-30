from django.db import models
from .model_mixins import WagtailRevisionMixin
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField

class ProductCategory(WagtailRevisionMixin, models.Model):
    title = models.CharField(max_length=255)

    panels = [FieldPanel("title")]
    api_fields = [APIField("title")]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "product category"
        verbose_name_plural = "product categories"
