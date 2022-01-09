from django.urls import path 
from .views.views import *
from .views.views import Profile as ProfileModel
from .views.apiviews import *

urlpatterns = [
    # -- Web View Urls
    path('login-web', Login.as_view(), name="login"),
    path('register-web/', Register.as_view(), name="register"),
    path('verify-email/<uid64>/<token>', VerifyEmail.as_view(), name="verify-email"),
    path('logout-web', logout, name="logout"),
    path('profile-web', ProfileModel.as_view(), name="profile"), 
    
    # -- API View Urls
    path('register/', RegisterApiView.as_view(), name="register-api"),
    path('login/', LoginApiView.as_view(), name="login-api"),
    path('profile/', ProfileAPIView.as_view(), name="profile-api"),
    path('profile/<int:pk>', ProfileDetailApiView.as_view(), name="profile-detail"),  
    
]