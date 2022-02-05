from datetime import timezone
from api.serializers.order_serializer import *
from rest_framework import generics, permissions, status, response, views


# -- Cartitem list
class CartItemListApiView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    
# -- add to cart
class AddToCart(views.APIView):
    def post(self, request):
        if request.user.is_authenticated:
            slug = request.data['slug', None]
            if slug is None:
                return response.Response({'message': 'Invalid slug request'}, status=status.HTTP_400_BAD_REQUEST)
            
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
            
            if request.method == "POST":
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
                
                return response.Response({'message': 'Invalid slug request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        


# -- Get coupon
class CouponListApiView(generics.ListAPIView):
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
    permission_classes = (permissions.IsAuthenticated,)



# -- shipping address
class ShippingAddressApiView(generics.ListCreateAPIView):
    serializer_class = ShippingAddressSerializer
    queryset = ShippingAddress.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self):
        return self.serializer_class.save()
    
# -- remove shipping address api 
class RemoveShippingAddressApi(generics.DestroyAPIView):
    serializer_class = ShippingAddressSerializer
    queryset = ShippingAddress.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    
class OrderListApiView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    
class UpdateOrderApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated,)