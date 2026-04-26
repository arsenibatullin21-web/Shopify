import copy
from decimal import Decimal

from aiohttp import request
from django.shortcuts import get_object_or_404

from Shopify import settings
from main.models import Product, PromoCode


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart


    def add(self, product , size=None, color=None, quantity=1,override_quantity=False):
        cart_key = f"{product.id}_{size.id}_{color.id}"
        if cart_key not in self.cart:
            self.cart[cart_key] = {'product_id': product.id,
                                    'quantity': 0,
                                     'price': str(product.get_discount_price()),
                                     'size_id': size.id,
                                     'size_name': str(size),
                                     'color_id': color.id,
                                     'color_name': str(color)
                                     }
        if override_quantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, cart_key):
        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        cart = copy.deepcopy(self.cart)

        for key, item in cart.items():
            item['cart_key'] = key

        for product in products:
            for item in cart.values():
                if item['product_id'] == product.id:
                    item['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]

    def clear_items(self):
        self.session['cart'] = {}
        self.save()

    def get_total_price(self, code=None):
        if code:
            self.request.session['promo_id'] = code.id
        else:
            self.request.session['promo_id'] = None
        if code:
            total = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
            total = total - (total * Decimal(code.discount / 100))
        else:
            total = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        return format(total, '.2f')

    def update_quantity(self, cart_key, action):
        if cart_key in self.cart:
            if action == 'increase':
                self.cart[cart_key]['quantity'] += 1
            elif action == 'decrease':
                self.cart[cart_key]['quantity'] -= 1

                if self.cart[cart_key]['quantity'] <= 0:
                    del self.cart[cart_key]
        self.save()











