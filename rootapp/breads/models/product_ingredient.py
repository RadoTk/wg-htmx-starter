from django.db import models
from wagtail.models import DraftStateMixin
from .model_mixins import WagtailRevisionMixin
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField

class ProductIngredient(DraftStateMixin, WagtailRevisionMixin, models.Model):
    name = models.CharField(max_length=255)

    panels = [FieldPanel("name")]
    api_fields = [APIField("name")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "product ingredient"
        verbose_name_plural = "product ingredients"
