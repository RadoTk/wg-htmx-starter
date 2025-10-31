# models/pages.py

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.images.models import Image
from wagtail.models import (
    Page,
    
)

from .blocks import BaseStreamBlock
from rootapp.base import models  # Si tu utilises des blocs pour la mise en page

class StandardPage(Page):
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(BaseStreamBlock(), verbose_name="Page body", blank=True, use_json_field=True)

class HomePage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )
    hero_text = models.CharField(max_length=255, help_text="Write an introduction for the bakery")
    # Autres champs et panels pour le contenu de la homepage
