from decimal import Decimal
from django.shortcuts import render

from django.shortcuts import redirect, render
from django.urls import reverse

from django.template.loader import render_to_string
from rootapp.cart.cart import Cart
from rootapp.orders.forms import OrderCreateForm
from .models import Order, OrderItem, OrderStatus
from django.http import HttpRequest, HttpResponse, QueryDict

from django.http import JsonResponse



def create_cart_order_items(
        order: Order,
        cart: Cart,
) -> None:
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product_title=item["product_title"],
            product_id=item["product_id"],
            price=item["price"],
            quantity=item["quantity"],
        )

   
def order_create(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    shipping_cost = Decimal("0.00")
    subtotal = cart.get_subtotal_cost()
    total = subtotal + shipping_cost

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            create_cart_order_items(order, cart)
            cart.clear()
            return redirect("orders:order_thanks")
    else:
        form = OrderCreateForm()

    return render(
        request,
        "orders/create.html",
        {
            "cart": cart,
            "form": form,
            "shipping_cost": shipping_cost,
            "subtotal": subtotal,
            "total": total,
        }
    )


def order_thanks(request):
    return render(request, 'orders/thanks.html')



def refresh_order_badge(request):
    status = OrderStatus.objects.filter(code='new', is_active=True).first()
    count = Order.objects.filter(status=status).count() if status else 0
    return JsonResponse({'count': count})

