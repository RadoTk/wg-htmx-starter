from django.db import models
from django.http import HttpRequest
from modelcluster.fields import ParentalKey  # type: ignore
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page

from rootapp.cart.forms import CartAddProductForm
#FIXE(AR): from common.models import DrupalFields


class StoreIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["base.HomePage"]
    subpage_types: list[str] = [
        "store.StoreProductIndexPage",
    ]

    max_count = 1

    def get_context(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        context = super().get_context(request)

        context["products"] = Product.objects.all().order_by("-is_featured", "title")
        context["cart_add_product_form"] = CartAddProductForm()

        return context
    

class StoreProductIndexPage(Page):
    max_count = 1
    parent_page_types = [
        "store.StoreIndexPage",
    ]
    subpage_types = ["store.Product"]

    def get_context(self, request):
        context = super().get_context(request)
        context["products"] = self.get_children().type(Product).live()
        return context



#FIXE(AR): concept de DrupalFields, à ajouter (depuis la source)
class Product(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    description = RichTextField(blank=True)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    parent_page_types = ["store.StoreProductIndexPage"]
    subpage_types: list[str] = []

    content_panels = Page.content_panels + [
        FieldPanel("description", classname="full"),
        FieldPanel("price_usd"),
        FieldPanel("available"),
        FieldPanel("is_featured"),
        FieldPanel("image"),
    ]

    def get_context(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        context = super().get_context(request)

        context["cart_add_product_form"] = CartAddProductForm()

        return context

    @property
    def price(self) -> str:
        """Alias of price_usd for backwards compatibility."""
        return self.price_usd

