from django.shortcuts import render
# from . sub_models.cart_models import *


def cart(request):
    return render(request, 'cart.html')