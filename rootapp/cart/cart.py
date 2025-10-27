from decimal import Decimal
from collections.abc import Generator

from django.conf import settings
from django.http import HttpRequest
from rootapp.store.models import StoreProduct
from .models import Cart as CartModel, CartItem


class Cart:
    """
    Gestion hybride du panier : session pour visiteurs, DB pour utilisateurs connectés.
    Fournit un point d'entrée unique pour toutes les apps (store, orders, checkout).
    """

    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        self.user = getattr(request, "user", None)
        self.session_cart = self.session.get(settings.CART_SESSION_ID, {})

        # Panier DB si utilisateur connecté
        if self.user and self.user.is_authenticated:
            self.db_cart, _ = CartModel.objects.get_or_create(user=self.user)
            if self.session_cart:
                self.merge_session_cart()
        else:
            self.db_cart = None

    # -----------------
    # Ajouter ou mettre à jour un produit
    # -----------------
    def add(self, product: StoreProduct, quantity: int = 1, save_db=True, replace_quantity=False) -> None:
        if self.db_cart:
            item, created = CartItem.objects.get_or_create(
                cart=self.db_cart,
                product=product,
                defaults={"price": product.price}
            )
            if not created:
                if replace_quantity:
                    item.quantity = quantity  
                else:
                    item.quantity += quantity  
            else:
                item.quantity = quantity
            item.price = product.price
            item.save()
        else:
            product_id = str(product.id)
            if product_id in self.session_cart:
                if replace_quantity:
                    self.session_cart[product_id]["quantity"] = quantity
                else:
                    self.session_cart[product_id]["quantity"] += quantity
            else:
                self.session_cart[product_id] = {
                    "product_title": product.title,
                    "product_id": product_id,
                    "quantity": quantity,
                    "price": str(product.price),
                }
            self.save_session()


    # -----------------
    # Supprimer un produit
    # -----------------
    def remove(self, product: StoreProduct) -> None:
        if self.db_cart:
            CartItem.objects.filter(cart=self.db_cart, product=product).delete()
        else:
            product_id = str(product.id)
            if product_id in self.session_cart:
                del self.session_cart[product_id]
                self.save_session()

    # -----------------
    # Vider le panier
    # -----------------
    def clear(self) -> None:
        if self.db_cart:
            self.db_cart.items.all().delete()
        self.clear_session()

    # -----------------
    # Fusionner session → DB
    # -----------------
    def merge_session_cart(self) -> None:
        for product_id, item in self.session_cart.items():
            product = StoreProduct.objects.get(id=product_id)
            self.add(product, item["quantity"])
        self.clear_session()

    # -----------------
    # Gestion session
    # -----------------
    def save_session(self) -> None:
        self.session[settings.CART_SESSION_ID] = self.session_cart
        self.session.modified = True

    def clear_session(self) -> None:
        self.session_cart = {}
        self.save_session()

    # -----------------
    # Itérateur pour templates/API
    # -----------------
    def __iter__(self) -> Generator:
        if self.db_cart:
            for item in self.db_cart.items.all():
                yield {
                    "product": item.product,
                    "quantity": item.quantity,
                    "price": item.price,
                    "total_price": item.get_total_price(),
                }
        else:
            product_ids = self.session_cart.keys()
            products = StoreProduct.objects.filter(id__in=product_ids)
            for product in products:
                item = self.session_cart[str(product.id)].copy()
                item["product"] = product
                item["price"] = Decimal(item["price"])
                item["total_price"] = item["price"] * item["quantity"]
                yield item

    # -----------------
    # Nombre total d’articles
    # -----------------
    def __len__(self) -> int:
        if self.db_cart:
            return sum(item.quantity for item in self.db_cart.items.all())
        else:
            return sum(item["quantity"] for item in self.session_cart.values())

    # -----------------
    # Sous-total et total
    # -----------------
    def get_cart_subtotal(self) -> Decimal:
        if self.db_cart:
            return sum(item.get_total_price() for item in self.db_cart.items.all())
        else:
            return sum(
                Decimal(item["price"]) * item["quantity"]
                for item in self.session_cart.values()
            ).quantize(Decimal("0.01"))

    def get_cart_total(self) -> Decimal:
        # Ici on pourrait ajouter shipping, taxes, etc.
        return self.get_cart_subtotal()

    # -----------------
    # Liste uniforme pour templates/API
    # -----------------
    def get_items(self) -> list[dict]:
        return list(self.__iter__())
