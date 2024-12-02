from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view(),name="loginuser"), 
    path('signup/', Signup.as_view(),name="signupuser"),
    path('forget/', Forget.as_view(),name="forgetuser"),
    path('reset/<uuid:uuid>', Reset.as_view(),name="resetuser"),
    path('dashboard/', Dashboard.as_view(),name="dashboarduser"),
    path('detail/', Detail.as_view(),name="detailuser"),
    path('logout/', Logout.as_view(),name="logoutuser"),
]
