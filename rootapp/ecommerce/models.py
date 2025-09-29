from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class ProductPage(Page):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('image'),
    ]

class ProductIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
            context = super().get_context(request)
            context['products'] = ProductPage.objects.child_of(self).live()
            return context
    
    subpage_types = ['ecommerce.ProductPage']
            