from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from pydantic.types import Decimal

from cart.cart import Cart
from main.models import Size, Color, PromoCode
from orders.forms import OrderCreateForm
from orders.models import OrderItem


@login_required
def order_create(request):
    cart = Cart(request)
    promo_id = request.session.get('promo_id')
    code = PromoCode.objects.filter(id=promo_id).first()
    discount_rate = Decimal('0')


    if code:
        discount_rate = Decimal(str(code.discount)) / Decimal('100')


    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request=request)
        if form.is_valid():
            order = form.save()
            for item in cart:
                discounted_price = item['product'].get_discount_price()
                discounted_price = discounted_price - (discounted_price * discount_rate)
                size = Size.objects.filter(id=item['size_id']).first()
                color = Color.objects.filter(id=item['color_id']).first()

                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         product_name=item['product'].name,
                                         price=discounted_price,
                                         quantity=item['quantity'],
                                         size=size,
                                         size_name=item['size_name'],
                                         color=color,
                                         color_name=item['color_name'],
                                         discount=item['product'].discount,
                                         )
            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm(request=request)
    return render(request, 'orders/create_order.html', {'cart': cart, 'form': form, 'total_price': cart.get_total_price(code=code), 'promo': code })