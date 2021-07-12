from django.db import models

class ProductCategory(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/products', null=True , blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=60, blank=True, null=True)
    discount_price = models.DecimalField(decimal_places=2, max_digits=60, blank=True, null=True)
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


class ProductReview(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    name =  models.CharField(max_length=250, null=False, blank=False)
    email =  models.CharField(max_length=250, null=False, blank=False)
    message =  models.TextField(null=False, blank=False)
    date =  models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.name + "  |  " + str(self.product_id.title)


class VariationManager(models.Model):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')


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