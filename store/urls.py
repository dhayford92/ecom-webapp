
from django.urls import path
from . views import *


urlpatterns = [
    path('', home, name="home"),
    path('shop/', store, name="store"),
    path('?P<slug:slug>.+?', ProductDetail, name="detail"),
    path('?P<str:title>.+?/', category, name="category"),
    path('?P/s/.+?', search, name="search"),
]