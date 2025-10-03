from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from rootapp.store.models import Product, StoreIndexPage
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd["quantity"])
        cart.save()

    # Si c’est via HTMX, renvoyer le fragment panier
    if request.headers.get('Hx-Request'):
        html = render_to_string("cart/_cart_summary.html", {"cart": cart}, request=request)
        return HttpResponse(html)

    return redirect("cart:cart_detail")

@require_GET
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if request.headers.get('Hx-Request'):
        html = render_to_string("cart/_cart_summary.html", {"cart": cart}, request=request)
        return HttpResponse(html)

    return redirect("cart:cart_detail")

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        qty = cd["quantity"]
        if qty <= 0:
            cart.remove(product)
        else:
            cart.add(product=product, quantity=qty)
        cart.save()

    if request.headers.get('Hx-Request'):
        html = render_to_string("cart/_cart_summary.html", {"cart": cart}, request=request)
        return HttpResponse(html)

    return redirect("cart:cart_detail")

@require_GET
def cart_detail(request):
    cart = Cart(request)
    store_index_page = StoreIndexPage.objects.first()
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(initial={"quantity": item["quantity"]})
    context = {"cart": cart, "store_index_page": store_index_page}
    return render(request, "cart/cart_detail.html", context)
