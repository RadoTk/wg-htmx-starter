from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from rootapp.store.models import Product 

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Logique de panier ici (ex: session or DB)
    request.session.setdefault('cart', {})
    cart = request.session['cart']
    cart[str(product_id)] = {'quantity': quantity}
    request.session.modified = True

    return redirect('cart:detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    return render(request, 'cart/cart_detail.html', {'cart': cart})
