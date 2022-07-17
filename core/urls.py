from django.urls import path
from . views import *


urlpatterns = [
    path('cart/', cart, name="cart"),
    path('add_cart/<slug:slug>', add_cart, name="add_cart"),
    path('remove-from-cart/<slug:slug>', remove_from_cart, name="remove_from_cart"),
    path('checkout', CheckOut.as_view(), name="checkout"),
    path('add_coupon', add_coupon, name="add_coupon"),
    path('payment', PaymentView.as_view(), name="payment"),
]