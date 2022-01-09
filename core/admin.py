from django.contrib import admin
from .models import *


class OrderAmdin(admin.ModelAdmin):
    list_display = ('orderID', 'order_status', 'order_type', 'shipaddress', 'ordered', 'created_on')
    search_fields = ('orderID', 'user__email')
    list_editable = ('order_status', 'shipaddress')
    date_hierarchy = 'created_on'
    list_filter = ('order_status', 'order_type', 'ordered')
    class Meta:
        model = Order

admin.site.register(CartItem)
admin.site.register(Coupon)
admin.site.register(Order, OrderAmdin)
admin.site.register(ShippingAddress)