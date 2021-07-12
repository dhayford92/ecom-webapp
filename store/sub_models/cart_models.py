from django.db import models
from store.models import *

class Cart(models.Model):
    products = models.ManyToManyField(Product)
    total = models.DecimalField(decimal_places=2, max_digits=60, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Cart id %s" %(self.id)