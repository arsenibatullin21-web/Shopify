from django.urls import path

from cart import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>', views.cart_add, name='cart_add'),
    path('update<str:cart_key>', views.cart_update_quantity, name='cart_update_quantity'),
    path('remove/<str:cart_key>', views.cart_remove, name='remove_cart'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('promo/', views.cart_promo, name='cart_promo')
]