from decimal import Decimal
from collections.abc import Generator

from django.conf import settings
from django.http import HttpRequest

#FIXE(AR): Tout ce qui concerne Shipping a commenter, fonctionnalité en attente / from shipping.calculator import get_book_shipping_cost
from rootapp.store.models import StoreProduct


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        """Initialize the cart."""
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(
        self,
        product: StoreProduct,
        quantity: int = 1,
    ) -> None:
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)  

        self.cart[product_id] = {
            "product_title": product.title,
            "product_id": product_id,
            "quantity": quantity,
            "price": str(product.price),
        }

        self.save()

    def save(self) -> None:
        """Sauvegarde le panier dans la session."""
        for item in self.cart.values():
            if isinstance(item.get("price"), Decimal):
                item["price"] = str(item["price"])
            if isinstance(item.get("total_price"), Decimal):
                item["total_price"] = str(item["total_price"])
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


    def remove(self, product: StoreProduct) -> None:
        """Remove a product from the cart."""
        product_id = str(product.id)  

        if product_id in self.cart:
            del self.cart[product_id]

            self.save()

    def get_products_in_cart(self) -> list[StoreProduct]:
        """Retourne la liste des objets Product présents dans le panier."""
        product_ids = self.cart.keys()
        return StoreProduct.objects.filter(id__in=product_ids)

    def get_cart_total(self) -> Decimal:
        """Retourne le coût total du panier (sous-total + éventuels frais)."""
        int_sum = sum(
            [
                self.get_cart_subtotal(),
                #self.get_shipping_cost(),
            ],
        )
        return Decimal(int_sum).quantize(Decimal("0.01"))

    def get_cart_subtotal(self) -> Decimal:
        totals = [
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        ]
        product_sum = sum(totals)
        return Decimal(product_sum).quantize(Decimal("0.01"))

    # FIXE(AR): A revoir, 
    # def get_shipping_cost(self) -> Decimal:
        # book_quantity = sum(item["quantity"] for item in self.cart.values())
        # return get_book_shipping_cost(book_quantity)

    def clear(self) -> None:
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]

        self.cart = {}

        self.save()

    def __iter__(self) -> Generator:
        """Get cart products from the database."""
        products = self.get_products_in_cart()
        cart_copy = {}

        for product in products:
            item = self.cart[str(product.id)].copy()

            item["product"] = product
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]

            cart_copy[str(product.id)] = item

            yield item


    def __len__(self) -> int:
        """Count all items in the cart."""

        # TODO: determine whether this should count the number of products
        # or the total quantity of products
        item_quantities = [item["quantity"] for item in self.cart.values()]

        return sum(item_quantities)
