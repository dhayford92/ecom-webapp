from django.urls import path 
from .views import *
from .views import Profile as ProfileModel

urlpatterns = [
    # -- Web View Urls
    path('login-web', Login.as_view(), name="login"),
    path('register-web/', Register.as_view(), name="register"),
    path('verify-email/<uid64>/<token>', VerifyEmail.as_view(), name="verify-email"),
    path('logout-web', logout, name="logout"),
    path('profile-web', ProfileModel.as_view(), name="profile"), 
    
    
    
]