from django.contrib import admin
from . models import*


class ProductAmdin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'price', 'discount_price', 'active', 'created_on')
    search_fields = ('title', 'slug')
    list_editable = ('title', 'price', 'discount_price', 'active')
    date_hierarchy = 'created_on'
    list_filter = ('active', 'price', 'discount_price')
    prepopulated_fields = {'slug': ('title', 'price')}
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


class VariationeAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'title', 'category', 'active','price', 'updated')
    search_fields = ['product_id', 'title']
    list_editable = ('title', 'category', 'active')
    date_hierarchy = 'updated'
    list_filter = ('product_id','active', 'category', 'price')
    class Meta:
        model = Variation


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rate', 'like', 'created_on')
    search_fields = ['user', 'product']
    date_hierarchy = 'created_on'
    list_filter = ('like', 'rate')
    class Meta:
        model = Review


admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Product, ProductAmdin)
admin.site.register(ProductsImage, ImageAdmin)
admin.site.register(Variation, VariationeAdmin)
admin.site.register(Review, ReviewAdmin)



