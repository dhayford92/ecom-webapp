from dataclasses import fields
from rest_framework import serializers
from core.models import *


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        depth = 1
        fields = '__all__'
        read_only_fields = ['id']
        

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
        
        
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        depth=1
        fields = '__all__'
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        depth=1
        fields = '__all__'
        read_only_fields = ['id', 'orderID']
        