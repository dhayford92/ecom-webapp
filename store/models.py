from django.db import models

from authentication.models import User

class ProductCategory(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/products', null=True , blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=60, default=0.0, blank=True, null=True)
    discount_price = models.DecimalField(decimal_places=2, max_digits=60, default=0.0, blank=True, null=True)
    category = models.ManyToManyField('ProductCategory', default='uncategorize', related_name='productcategory')
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
        
    class Meta:
        unique_together = ('title', 'slug')


class ProductsImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products')
    featured = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product_id.title



class VariationManager(models.Model):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')
    
    def packages(self):
        return self.all().filter(category='package')


VAR_CATEGORY = (
    ('color', 'color'),
    ('size', 'size'),
    ('package', 'package')
)


class Variation(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=120, choices=VAR_CATEGORY, default='size', null=True, blank=True)
    image = models.ForeignKey(ProductsImage, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    objects = VariationManager()

    def __str__(self):
        return self.product_id.title


RATE_CHOICES = (
    zip(range(1,6), range(1,6))
)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    like = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "Review id %s" %(self.user.name)
    
    
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.name + "  " + self.product.title