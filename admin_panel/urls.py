from django.urls import path 
from .views import*
from .product_views import*

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('manage-product', manage_product, name="manage_product"),
    path('add-product', add_product, name="add_product"),
    path('add-image', add_image, name="add_image"),
    path('add-variation', add_variation, name="add_variation"),
    path('product-detail/<int:id>', product_detail, name="product_detail"),
]