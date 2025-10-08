from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from decimal import Decimal
from django.utils.html import mark_safe


class Order(ClusterableModel):
    shopper_first_name = models.CharField(max_length=255, default="", blank=True)
    shopper_name = models.CharField(max_length=255, default="", blank=True)
    shopper_email = models.EmailField()
    shopper_address = models.CharField(max_length=255)
    shopper_postal_code = models.CharField(max_length=16)
    shopper_city = models.CharField(
        max_length=255,
        choices=[
            ("MG", "Madagascar"),
            ("FR", "France"),
            ("US", "United States"),
            # ... autres pays
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("shopper_first_name"),
            FieldPanel("shopper_name"),
            FieldPanel("shopper_email"),
        ], heading="Shopper"),
        MultiFieldPanel([
            FieldPanel("shopper_address"),
            FieldPanel("shopper_postal_code"),
            FieldPanel("shopper_city"),
        ], heading="Recipient"),
        InlinePanel("items", label="Produits commandés"),
    ]

    def __str__(self):
        return f"Order {self.id}"

    @property
    def shopper_full_name(self) -> str:
        return f"{self.shopper_first_name} {self.shopper_name}".strip()

    def get_total_items_cost(self) -> Decimal:
        return sum(item.get_cost() for item in self.items.all()).quantize(Decimal("0.01"))

    def formatted_items_table(self):
        if not self.items.exists():
            return "Aucun produit dans cette commande."

        rows = [
            f"<tr><td>{item.product_title}</td><td>{item.quantity}</td><td>{item.price} €</td><td>{item.get_cost()} €</td></tr>"
            for item in self.items.all()
        ]
        total = self.get_total_items_cost()
        table_html = f"""
            <table style="border-collapse: collapse; width: 100%; margin-top: 10px;">
                <thead>
                    <tr style="background-color: #0000FF;">
                        <th style="padding: 8px; border: 1px solid #ddd;">Produit</th>
                        <th style="padding: 8px; border: 1px solid #ddd;">Quantité</th>
                        <th style="padding: 8px; border: 1px solid #ddd;">Prix unitaire</th>
                        <th style="padding: 8px; border: 1px solid #ddd;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="3" style="padding: 8px; border: 1px solid #ddd; text-align: right;"><strong>Total</strong></td>
                        <td style="padding: 8px; border: 1px solid #ddd;"><strong>{total} €</strong></td>
                    </tr>
                </tfoot>
            </table>
        """
        return mark_safe(table_html)

    formatted_items_table.short_description = "Produits commandés"


class OrderItem(Orderable):
    order = ParentalKey(Order, related_name="items", on_delete=models.CASCADE)
    product_title = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    panels = [
        FieldPanel("product_title"),
        FieldPanel("price"),
        FieldPanel("quantity"),
    ]

    def __str__(self):
        return f"{self.quantity}x {self.product_title} @ {round(self.price, 2)} €/each"

    def get_cost(self) -> Decimal:
        return (self.price * self.quantity).quantize(Decimal("0.01"))
