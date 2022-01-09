from django.http import request
from authentication.models import Profile
from store.models import Product, Variation
from .models import ORDER_TYPE, CartItem, Coupon, ShippingAddress, Order
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages



def cart(request):
        if(request.user.is_authenticated):
            try:
                cart = Order.objects.get(user=request.user, ordered=False)
                cartitems = CartItem.objects.filter(user=request.user, ordered=False)
                empty_message = None
                empty = False
            except ObjectDoesNotExist:
                empty = True
                cart = None
                cartitems = None
                empty_message = "Your cart is empty, Please keep shopping."
            context = {
                "empty": empty, 
                "cart": cartitems,
                "items": cart,
                "empty_message": empty_message
                }
            return render(request, 'store/cart.html', context)
        else:
            return HttpResponseRedirect(reverse("login"))


def add_cart(request, slug):
    if request.user.is_authenticated:
        item = Product.objects.get(slug=slug)
        cart_item, created = CartItem.objects.get_or_create(item=item, user=request.user, ordered=False)
        cart_qs = Order.objects.filter(user=request.user, ordered=False)
        
        if cart_qs.exists():
            cart = cart_qs[0]
            if cart.items.filter(item__slug=item.slug).exists():
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart.items.add(cart_item)
        else:
            created_on = timezone.now()
            cart = Order.objects.create(user=request.user, created_on=created_on)
            cart.items.add(cart_item)
        
        if request.methed == "POST":
            qty = request.POST.get('qty')
            size = request.POST.get('size')
            color = request.POST.get('color')
            package = request.POST.get('package')
            for items in request.POST:
                key = items
                val = request.POST[key]
                try:
                    v = Variation.objects.get(id=val)
                except:
                    pass
            
            return HttpResponseRedirect(reverse("cart"))
    else:
        return HttpResponseRedirect(reverse("login"))



#removing item from cart
def remove_from_cart(request, slug):
    item = Product.objects.get(slug=slug)
    cart_item = CartItem.objects.get(item=item, user=request.user, ordered=False)
    cart_qs = Order.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        cart =  cart_qs[0]
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart.items.delete(cart_item)
            messages.success(request, 'Item removed')
    return HttpResponseRedirect(reverse("cart"))



class CheckOut(View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        cart = Order.objects.get(user=request.user, ordered=False)
        cartitems = CartItem.objects.filter(user=request.user, ordered=False)
        context = {
            "cart": cartitems,
            "items": cart,
            "profile": profile,
            "order_type": ORDER_TYPE,
        }
        return render(request, 'store/checkout.html', context)
    
    def post(self, request):
        number = request.POST.get('number')
        country = request.POST.get('country')
        city = request.POST.get('city')
        address = request.POST.get('address')
        order_type = request.POST.get('ordertype')
        order_qs = Order.objects.get(user=request.user, ordered=False)
        try:
            shipaddress = ShippingAddress(user=self.request.user, country=country, city=city, address=address)
            profile = Profile.objects.get(user=request.user)
            profile.number = number
            profile.save()
            shipaddress.save()
            order_qs.shipaddress = shipaddress
            order_qs.order_type = order_type
            order_qs.save()
            return render(request, 'store/checkout.html')
        except:
            messages.error(request, 'Error processing checkout order')
            return render(request, 'store/checkout.html')


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.error(request, 'This code does not exists')
        return reverse("checkout")


def add_coupon(request):
    if request.method == "POST":
        coupon = request.POST.get('coupon')
        order = Order.objects.get(user=request.user, ordered=False)
        try:
            order.coupon = get_coupon(request, coupon)
            order.save()
            messages.success(request, 'Coupon Added Successfully')
            return HttpResponseRedirect(reverse("checkout"))
        except ObjectDoesNotExist:
            messages.error(request, 'You do not have an active coupon')
            return HttpResponseRedirect(reverse("checkout"))
