from django.http import request
from authentication.models import Profile
from store.models import Product, Variation
from .models import ORDER_TYPE, CartItem, Coupon, PaymentModel, ShippingAddress, Order
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import stripe


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


# -- adding item to cart
def add_cart(request, slug):
    if request.user.is_authenticated:
        item = Product.objects.get(slug=slug)
        cart_item, created = CartItem.objects.get_or_create(item=item, user=request.user, ordered=False)
        cart_qs = Order.objects.filter(user=request.user, ordered=False)
        
        if request.method == "POST":
            qty = request.POST.get('qty')
            if cart_qs.exists():
                cart = cart_qs[0]
                if cart.items.filter(item__slug=item.slug).exists():
                    cart_item.quantity += qty
                    cart_item.save()
                else:
                    cart.items.add(cart_item)
            else:
                created_on = timezone.now()
                cart = Order.objects.create(user=request.user, created_on=created_on)
                cart.items.add(cart_item)
        else:
            print('error messages')
        
        # if request.method == "POST":
        #     qty = request.POST.get('qty')
        #     size = request.POST.get('size')
        #     color = request.POST.get('color')
        #     package = request.POST.get('package')
        #     for items in request.POST:
        #         key = items
        #         val = request.POST[key]
        #         try:
        #             v = Variation.objects.get(id=val)
        #         except:
        #             pass
            
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
        if cart.items.filter(item__slug=item.slug).exists():
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart.items.filter(id=cart_item.id).delete()
                if cart.items.count() == 0:
                    cart.delete()
                messages.success(request, 'Item removed')
        else:
            messages.error(request, 'Item not found')
    return HttpResponseRedirect(reverse("cart"))



#--check out view class
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
        try:
            order_qs = Order.objects.get(user=request.user, ordered=False)
            shipaddress = ShippingAddress(user=self.request.user, country=country, city=city, address=address)
            profile = Profile.objects.get(user=request.user)
            shipaddress.save()
            profile.number = number
            profile.save()
            order_qs.shipaddress = shipaddress
            order_qs.order_type = order_type
            order_qs.save()
            return HttpResponseRedirect(reverse("payment"))
        except:
            messages.error(request, 'Error processing checkout order')
            return HttpResponseRedirect(reverse("checkout"))


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.error(request, 'This code does not exists')
        return redirect("checkout")


def add_coupon(request):
    if request.method == "POST":
        coupon = request.POST.get('coupon')
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order.coupon = get_coupon(request, coupon)
            order.save()
            messages.success(request, 'Coupon Added Successfully')
            return redirect("checkout")
        except ObjectDoesNotExist:
            messages.error(request, 'You do not have an active coupon')
            return redirect("checkout")




class PaymentView(View):
    def get(self, request):
        orders = Order.objects.get(user=request.user, ordered=False)
        context = {
            "order": orders,
        }
        return render(request, 'store/payment.html', context)
    
    
    def post(self, request): 
        token = request.POST.get('stripeToken')
        try:
            orders = Order.objects.get(user=request.user, ordered=False)
            amount = orders.get_total() * 100
            stripe.api_key = 'sk_test_26PHem9AhJZvU623DfE1x4sd'
            charge = stripe.Charge.create(
                amount= amount,
                currency='usd',
                source=token,
            )
            # -- saving payment session
            payment = PaymentModel()
            payment.strip_id = charge['id']
            payment.user = request.user
            payment.amount = orders.total
            payment.save()
            # -- order complete session
            orders.payment = payment
            orders.ordered = True
            orders.save()
            messages.success(request, 'Your order was Successfully')
            return HttpResponseRedirect(reverse("home"))
        
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, f"{err.get('message')}")
        except stripe.error.RateLimitError as e:
            messages.error(request, "Rate limit error")
        except stripe.error.InvalidRequestError as e:
            messages.error(request, 'Invalid parameters')
        except stripe.error.AuthenticationError as e:
            messages.error(request, 'Not authenticated')
        except stripe.error.APIConnectionError as e:
            messages.error(request, 'Network error')
        except stripe.error.StripeError as e:
            messages.error(request, 'Something went wrong. You were not charged so please try again')
        except Exception as e:
            messages.error(request, 'Internal Error occured, We have been notified')
        return HttpResponseRedirect(reverse("payment"))