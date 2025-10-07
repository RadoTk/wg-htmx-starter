from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from decimal import Decimal

class Order(ClusterableModel):
    shopper_first_name = models.CharField(max_length=255, default="", help_text="First name of shopper.", blank=True)
    shopper_name = models.CharField(max_length=255, default="", help_text="First name of shopper.", blank=True)
    shopper_email = models.EmailField(help_text="Shopper email")
    shopper_address = models.CharField(max_length=255, help_text="Shopper address")
    shopper_postal_code = models.CharField(max_length=16, help_text="postal code of shopper")
    shopper_city = models.CharField(
    max_length=255,
    help_text="Country shopper",
    choices=[
        ("US", "United States"),
        ("CA", "Canada"),
        ("GB", "United Kingdom"),
        ("FR", "France"),
        ("DE", "Germany"),
        ("IT", "Italy"),
        ("ES", "Spain"),
        ("CN", "China"),
        ("JP", "Japan"),
        ("IN", "India"),
        ("BR", "Brazil"),
        ("RU", "Russia"),
        ("AU", "Australia"),
        ("ZA", "South Africa"),
        ("NG", "Nigeria"),
        ("EG", "Egypt"),
        ("KE", "Kenya"),
        ("MX", "Mexico"),
        ("AR", "Argentina"),
        ("KR", "South Korea"),
        ("SA", "Saudi Arabia"),
        ("AE", "United Arab Emirates"),
        ("SG", "Singapore"),
        ("NL", "Netherlands"),
        ("BE", "Belgium"),
        ("SE", "Sweden"),
        ("CH", "Switzerland"),
        ("PL", "Poland"),
        ("TR", "Turkey"),
        ("MA", "Morocco"),
        ("DZ", "Algeria"),
        ("TN", "Tunisia"),
        ("MG", "Madagascar"),
    ],
)
    #shipper_cost = models.DecimalField(max_digits=10, decimal_places=2,)
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("shopper_first_name"),
            FieldPanel("shopper_name"),
            FieldPanel("shopper_email"),
        ],
            heading="Shopper",
        ),
        MultiFieldPanel([
            FieldPanel("shopper_address"),
            FieldPanel("shopper_postal_code"),
            FieldPanel("shopper_city"),
        ],
            heading="Recipient",
        ),
    ]

    def __str__(self) -> str:
        return f"Order {self.id}"
    
    def get_total_items_cost(self) -> Decimal:
        items_cost = sum(
            [item.get_cost() for item in self.items.all()],
        )
        return Decimal(items_cost).quantize(Decimal("0.01"))

    #FIXE(AR): ajout de shipping cost
    #def get_total_cost(self) -> Decimal:
        #return self.get_total_items_cost() + Decimal(self.shipping_cost)

    @property
    def shopper_full_name(self) -> str:
        full_name = ""
        if self.shopper_first_name:
            full_name += self.shopper_first_name + " "
        if self.shopper_name:
            full_name += self.shopper_name + " "
        return full_name.rstrip()


class OrderItem(Orderable):
    order = ParentalKey(
        Order, related_name="items",
        on_delete=models.CASCADE,
        blank=False,
    )
    product_title = models.CharField(max_length=255,)
    product_id = models.PositiveIntegerField(default=1,)
    price = models.DecimalField(max_digits=10, decimal_places=2,)
    quantity = models.PositiveIntegerField(default=1,)

    panels = [
        FieldPanel("product_title"),
        FieldPanel("price"),
        FieldPanel("quantity"),
    ]

    #Pour montrer comment cet objet est affiché en texte, resumé rapide de l'objet
    def __str__(self):
        return f"{self.quantity}x {self.product_title} @ {round(self.price, 2)}/each"
    
    def get_cost(self) -> Decimal:
        total_cost = self.price * self.quantity
        return Decimal(total_cost).quantize(Decimal("0.01"))
