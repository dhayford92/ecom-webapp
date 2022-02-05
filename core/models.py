from django.db import models
from store.models import *
from authentication.models import User
from django.db.models.signals import pre_save
from store.utils import unique_order_id_generator



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.title
    
    def sub_totalprice(self):
        return self.quantity * self.item.price
    
    def sub_totaldisprice(self):
        return self.quantity * self.item.discount_price
    
    def sub_totalsave(self):
        return self.sub_totalprice() - self.sub_totaldisprice()

    def final_price(self):
        if self.item.discount_price > 0:
            return self.sub_totaldisprice()
        return self.sub_totaldisprice()



class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Confirmed', 'Comfirmed'),
        ('Delivered', 'Delivered'),
        ('Refound', 'Refound'),
    )

ORDER_TYPE = (
        ('Pickup', 'Pickup'),
        ('Delivery', 'Delivery'),
    )


class ShippingAddress(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.userID + " " + self.country + " " + self.city


class Order(models.Model):
    orderID = models.CharField(max_length=100, unique=True, db_index=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, null=True, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=60, default=0.00)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS, default="Pending")
    order_type = models.CharField(max_length=100, choices=ORDER_TYPE, default="Pickup")
    note = models.TextField(null=True, blank=True)
    shipaddress = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return "Order ID :  %s" %(self.orderID)


    def get_cart_total(self):
        total = 0
        for item in self.items.all():
            total += item.final_price()
            if self.coupon:
                total -= self.coupon.discount
        return total




def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.orderID:
        instance.orderID = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)