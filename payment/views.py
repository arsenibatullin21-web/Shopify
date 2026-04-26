from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
import stripe
from django.urls import reverse
from decimal import Decimal

from main.models import PromoCode
from orders.models import Order

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    total_price = sum(item.price * item.quantity for item in order.items.all())


    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
        )
        canceled_url = request.build_absolute_uri(
            reverse('payment:canceled')
        )

        session_data = {
             'mode': 'payment',
             'client_reference_id': order_id,
             'success_url': success_url,
             'cancel_url': canceled_url,
             'line_items': []
        }
        description_parts = []

        for item in order.items.all():
            image_url = None
            if item.product and item.product.image:
                image_url = request.build_absolute_uri(item.product.image.url)

            if item.size_name:
                description_parts.append(f"Size: {item.size_name}")
            if item.color_name:
                description_parts.append(f"Color: {item.color_name}")
            if item.discount:
                description_parts.append(f"Discount: {item.discount}%")

            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product_name,
                        'description': ' | '.join(description_parts),
                        'images': [image_url] if image_url else [],
                    }
                },
                'quantity': item.quantity,
            })

        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())

def payment_completed(request):
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
