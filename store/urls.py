from store.sub_views.cartviews import cart
from django.urls import path
from . views import *
from .sub_views.authViews import * 
from .sub_views.api import *


urlpatterns = [
    path('', home, name="home"),
    path('shop/', store, name="store"),
    path('?P<slug:slug>.+?', ProductDetail, name="detail"),
    path('?P<str:title>.+?/', category, name="category"),
    path('?P/s/.+?', search, name="search"),
    path('cart', cart, name="cart"),

    # -- authentication urls ---
    path('login', login, name="login"),
    path('sign-in-user', signin , name="signin"),
    path('register/', register, name="register"),
    path('save-auth', save_register, name="save_register"),
    path('logout', logout, name="logout"),

    #  -- api urls here --
    path('api/product/v1', ProductView.as_view()),
    path('api/image/v1', ImageView.as_view()),
    path('api/category/v1', CategoryView.as_view()),
    path('api/review/v1', ReviewView.as_view()),
    path('api/variation/v1', VariationView.as_view()),
]