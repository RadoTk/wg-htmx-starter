from django.db import models
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from decimal import Decimal
from django.utils.html import mark_safe, format_html
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.exceptions import ValidationError


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = "Pays"

    def __str__(self):
        return self.name

class OrderStatus(models.Model):
    """
    Modèle pour gérer les statuts de commande
    """
    code = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#000000")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Statut de commande"
        verbose_name_plural = "Statuts de commande"
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name
    
    def colored_name(self):
        return format_html(
            '<span style="color: {};">●</span> {}',
            self.color,
            self.name
        )
    colored_name.short_description = "Statut"

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
    status = models.ForeignKey(
        OrderStatus,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Statut de la commande"
    )
    
    def __str__(self):
        status_name = self.status.name if self.status else "Nouvelle"
        return f"Commande {self.id} - {status_name}"
    
    def save(self, *args, **kwargs):
        if not self.status:
            try:
                default_status = OrderStatus.objects.filter(
                    is_active=True
                ).order_by('sort_order').first()
                if default_status:
                    self.status = default_status
            except:
                # En cas d'erreur (table non créée), on ignore
                pass
        super().save(*args, **kwargs)
    
    @property
    def status_color(self):
        return self.status.color if self.status else "#6c757d"
    
    @property 
    def status_name(self):
        return self.status.name if self.status else "Nouvelle"
    
    def colored_status(self):
        status_name = self.status_name
        color = self.status_color
        return format_html(
            '<span style="color: {}; font-weight: bold;">● {}</span>',
            color,
            status_name
        )
    colored_status.short_description = "Statut"
    
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


    def get_status_display_with_color(self):
        """Méthode pour afficher le statut avec couleur même en mode édition"""
        if self.status:
            return format_html(
                '<span style="color: {};">● {}</span>',
                self.status.color,
                self.status.name
            )
        return "Non défini"
    
    def get_allowed_status_transitions(self):
        current_code = self.status.code if self.status else "new"
        transitions = {
            "new": ["in_progress", "cancelled"],
            "in_progress": ["packaged", "cancelled"],
            "packaged": ["in_delivery"],
            "in_delivery": ["delivered"],
            "delivered": [],
            "cancelled": [],
        }
        return transitions.get(current_code, [])

    def clean(self):
        if self.pk:
            original = Order.objects.get(pk=self.pk)
            allowed = original.get_allowed_status_transitions()
            if self.status and self.status.code not in allowed:
                raise ValidationError(f"Transition vers '{self.status.name}' non autorisée depuis '{original.status.name}'.")


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