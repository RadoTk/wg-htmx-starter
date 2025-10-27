from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET

from rootapp.store.models import StoreProduct, StoreIndexPage
from .cart import Cart
from .forms import CartAddProductForm


def render_cart_summary(request, cart: Cart):
    """Helper pour HTMX ou mini-panier."""
    store_index_page = StoreIndexPage.objects.first()
    html = render_to_string(
        "cart/_cart_summary.html",
        {"cart": cart, "store_index_page": store_index_page},
        request=request,
    )
    return HttpResponse(html)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(StoreProduct, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        qty = form.cleaned_data["quantity"]
        cart.add(product, qty)

    if request.headers.get("Hx-Request"):
        return render_cart_summary(request, cart)

    return redirect("cart:cart_detail")


@require_GET
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(StoreProduct, id=product_id)
    cart.remove(product)

    if request.headers.get("Hx-Request"):
        return render_cart_summary(request, cart)

    return redirect("cart:cart_detail")


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(StoreProduct, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        qty = form.cleaned_data["quantity"]
        if qty <= 0:
            cart.remove(product)
        else:
            cart.add(product, qty, replace_quantity=True)

    if request.headers.get("Hx-Request"):
        return render_cart_summary(request, cart)

    return redirect("cart:cart_detail")


@require_GET
def show_cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(initial={"quantity": item["quantity"]})
    store_index_page = StoreIndexPage.objects.first()
    context = {"cart": cart, "store_index_page": store_index_page}
    return render(request, "cart/cart_detail.html", context)
