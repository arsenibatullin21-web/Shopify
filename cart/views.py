from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartProductAddForm
from main.models import Product, PromoCode


# Create your views here.




@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartProductAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'],
                 size=cd['size'],
                 color=cd['color'],
                 )
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'cart/partials/add_cart_response.html', {'cart': cart, 'total_price': cart.get_total_price()})
    else:
        return redirect(product.get_absolute_url())


@require_POST
def cart_remove(request, cart_key):
    cart = Cart(request)
    cart.remove(cart_key)
    if  request.headers.get('HX-Request') == 'true':
        return render(request, 'cart/partials/cart_response.html', {'cart': cart, 'total_price': cart.get_total_price() })
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart, 'total_price': cart.get_total_price() })

def cart_clear(request):
    cart = Cart(request)
    cart.clear_items()
    if request.htmx:
        return render(request, 'cart/partials/cart_response.html',{'total_price': cart.get_total_price() })
    return redirect('cart:cart_detail')


@require_POST
def cart_update_quantity(request, cart_key):
    cart = Cart(request)
    action = request.POST.get('action')
    cart.update_quantity(cart_key, action)
    if request.htmx:
        return render(request, 'cart/partials/cart_response.html', {'total_price': cart.get_total_price() })
    return redirect('cart:cart_detail')


def cart_promo(request):
    cart = Cart(request)
    promo_code = request.GET.get('promo', '')
    code = PromoCode.objects.filter(code=promo_code).first()
    total = cart.get_total_price(code=code)

    if request.htmx:
        return render(request, 'cart/partials/cart_response.html', {'promo': code, 'cart': cart, 'total_price': total})
    return redirect('cart:cart_detail')
