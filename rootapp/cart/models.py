# from django.conf import settings
# from django.db import models
# from rootapp.store.models import StoreProduct
# from decimal import Decimal

# class Cart(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def get_total(self):
#         return sum(item.get_total_price() for item in self.items.all())

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
#     product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def get_total_price(self):
#         return self.price * self.quantity



from django.conf import settings
from django.db import models
from rootapp.store.models import StoreProduct
from decimal import Decimal

# Fonction utilitaire pour calculer le total d'une liste d'items
def calculate_total(items):
    return sum(item.get_total_price() for item in items)

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        # On délègue le calcul à la fonction séparée
        return calculate_total(self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity
