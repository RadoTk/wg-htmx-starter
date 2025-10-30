from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField

class ProductOrigin(models.Model):
    title = models.CharField(max_length=100)

    panels = [FieldPanel("title")]
    api_fields = [APIField("title")]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "product origin"
        verbose_name_plural = "product origins"
