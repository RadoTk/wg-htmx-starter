from decimal import Decimal
from django.shortcuts import redirect, render
from rootapp.cart.cart import Cart
from rootapp.orders.forms import OrderCreateForm
from .models import Order, OrderItem, OrderStatus
from django.http import HttpRequest, HttpResponse, JsonResponse



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


def order_thanks_view(request):
    return render(request, 'orders/thanks.html')



def get_new_orders_count(request):
    status = OrderStatus.objects.filter(code='new', is_active=True).first()
    count = Order.objects.filter(status=status).count() if status else 0
    return JsonResponse({'count': count})

