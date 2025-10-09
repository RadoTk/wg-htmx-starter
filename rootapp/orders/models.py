from django.db import models
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from decimal import Decimal
from django.utils.html import mark_safe
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = "Pays"

    def __str__(self):
        return self.name

class BaseOrder(models.Model):
    shopper_first_name = models.CharField(max_length=255)
    shopper_name = models.CharField(max_length=255)
    shopper_email = models.EmailField()
    shopper_address = models.CharField(max_length=255)
    shopper_postal_code = models.CharField(max_length=16)
    shopper_country = models.ForeignKey(Country, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Order(BaseOrder, ClusterableModel):

    def __str__(self):
        return f"Order {self.id}"

    @property
    def shopper_full_name(self) -> str:
        return f"{self.shopper_first_name} {self.shopper_name}".strip()

    def get_total_items_cost(self) -> Decimal:
        total = sum(item.get_cost() for item in self.items.all())
        return total.quantize(Decimal("0.01"))

    def formatted_items_table(self):
        if not self.items.exists():
            return "Aucun produit dans cette commande."

        html = render_to_string("orders/includes/order_items_table.html", {"order": self})
        return mark_safe(html)

    formatted_items_table.short_description = "Produits commandés"


    def view_items_link(self):
        try:
            url = reverse("order:inspect", args=[self.pk])
        except Exception as e:
            return f"(Erreur de lien: {e})"
        return format_html('<a class="button button-small" href="{}">Voir produits</a>', url)

    view_items_link.short_description = "Produits"


class OrderItem(Orderable):
    order = ParentalKey(Order, related_name="items", on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product_title} @ {round(self.price, 2)} €/each"

    def get_cost(self) -> Decimal:
        return (self.price * self.quantity).quantize(Decimal("0.01"))
    
