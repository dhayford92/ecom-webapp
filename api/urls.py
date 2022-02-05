from django.urls import path
from api.views.order_views import *
from api.views.product_views import *
from .views.auth_views import *

urlpatterns = [
    # -- auth API View Urls
    path('register/', RegisterApiView.as_view(), name="register-api"),
    path('login/', LoginApiView.as_view(), name="login-api"),
    path('profile/', ProfileAPIView.as_view(), name="profile-api"),
    path('profile/<int:pk>', ProfileDetailApiView.as_view(), name="profile-detail"),  
     # -- products API View Urls
    path('category-api/', CategoryApiView.as_view(), name="category-api"),
    path('product-api/', ProductApiView.as_view(), name="product-api"),
    path('images-api/', ProductImageApiView.as_view(), name="images-api"),
    path('variation-api/', ProductVariationApiView.as_view(), name="variation-api"),
    path('favorite/add-list/', AddListFavoriteApiView.as_view(), name="add-list-favorite"),
    path('favorite/remove/<int:pk>', RemoveFromFavoriteApiView.as_view(), name="remove-favorite"),
    path('reviews/', ProductReviewApiView.as_view(), name="reviews"),
    # -- orders
    path('cart/cartlist/', CartItemListApiView.as_view(), name="cartlist"),
    path('cart/add-to-cart/', AddToCart.as_view(), name="add-to-cart"),
    path('coupon/', CouponListApiView.as_view(), name="coupon"),
    path('address/', ShippingAddressApiView.as_view(), name="address"),
    path('address/remove/<int:pk>', RemoveShippingAddressApi.as_view(), name="remove-address"),
    path('order/', OrderListApiView.as_view(), name="order-list"),
    path('order/update/<int:pk>', UpdateOrderApiView.as_view(), name="order-update"),
]

