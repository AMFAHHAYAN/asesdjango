from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', DashboardView.as_view(), name='dashboard'),
    path('', Landing.as_view(), name='landing'),
    path('prods/', Products.as_view(), name='list'),
    path('categries/', Categories.as_view(), name='catoglist'),
    path('subcategries/', Subcategories.as_view(), name='subcatlist'),
    path('prodform/', ProductFormView.as_view(), name='prodfrom'),
    path('catform/', CategoryFormView.as_view(), name='catform'),
    path('subcatform/', SubcategoryFormView.as_view(), name='subcatform'),
    path('users/', Users.as_view(), name='users'),
]