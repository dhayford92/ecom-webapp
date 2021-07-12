from django.contrib import admin
from . models import*
from . sub_models.cart_models import *


class ProductAmdin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'price', 'discount_price', 'active', 'created_on')
    search_fields = ('title', 'slug')
    list_editable = ('title', 'price', 'discount_price', 'active')
    date_hierarchy = 'created_on'
    list_filter = ('active', 'price', 'discount_price')
    prepopulated_fields = {'slug': ('title', 'id')}
    class Meta:
        model = Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ['title']
    list_editable = ['title']
    class Meta:
        model = ProductCategory


class ImageAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'active', 'featured', 'updated')
    search_fields = ['product_id']
    list_editable = ('featured', 'active')
    date_hierarchy = 'updated'
    list_filter = ('active', 'featured')
    class Meta:
        model = ProductsImage



admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Product, ProductAmdin)
admin.site.register(ProductsImage, ImageAdmin)
admin.site.register(Variation)
admin.site.register(ProductReview)



# ----Other model Admin -----
admin.site.register(Cart)