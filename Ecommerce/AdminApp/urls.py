
from django.urls import path
from .views import *

urlpatterns = [
    path('admindashboard/', DashboardView.as_view(), name='dashboard'),
    path('login/', AdminLogin.as_view(), name='adminlogin'),
    path('logout/', AdminLogout.as_view(), name='adminlogout'),
    path('', Landing.as_view(), name='landing'),
    path('prodform/', ProductFormView.as_view(), name='prodfrom'),
    path('catform/', CategoryFormView.as_view(), name='catform'),
    path('subcatform/', SubcategoryFormView.as_view(), name='subcatform'),   
    path('prods/', ProductListView.as_view(), name='product_list'),
    path('categries/', CategoryListView.as_view(), name='catoglist'),
    path('subcategries/', SubcategoryListView.as_view(), name='subcatlist'),
    path('deletcategory/<int:pk>', CategoryDeleteView.as_view(), name='catogdelete'),
    path('deletsubcategory/<int:pk>', SubcategoryDeleteView.as_view(), name='subcatogdelete'),
    path('proddelete/<int:pk>', ProductDeleteView.as_view(), name='prodelete'),
    # path('users/', Users.as_view(), name='users'),
]