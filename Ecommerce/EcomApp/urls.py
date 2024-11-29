from django.urls import path
from .views import *
urlpatterns = [
    path('', Landingpage.as_view(),name='landing'),
    
]