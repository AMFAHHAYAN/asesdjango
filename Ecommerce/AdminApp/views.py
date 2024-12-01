from django.shortcuts import render
from django.views import View
from .forms import ProductForm, CategoryForm, SubcategoryForm

class DashboardView(View):
    def get(self, request):
        return render(request, 'admin/dashboard.html')
    
class Landing(View):
    def get(self, request):
        return render(request, 'landing.html')
    
class Products(View):  # Capitalized to follow Python class naming conventions
    def get(self, request):
        return render(request, 'admin/prodlist.html')
    
class ProductFormView(View):  # Renamed to avoid conflict with form class
    def get(self, request):
        form = ProductForm()
        return render(request, 'admin/product-form.html', {'form': form})
    
class Users(View):
    def get(self, request):
        return render(request, 'admin/userlist.html')
    
class CategoryFormView(View):  # Renamed to avoid conflict
    def get(self, request):
        form = CategoryForm()  # Changed variable name to match form class
        return render(request, 'admin/categoryform.html', {'form': form})
class Categories(View):
    def get(self, request):
        return render(request, 'admin/categorylist.html')
    
class Subcategories(View):
    def get(self, request):
        return render(request, 'admin/subcategries.html')
    

class SubcategoryFormView(View):  # Renamed to avoid conflict
    def get(self, request):
        form = SubcategoryForm()  # Changed variable name to match form class
        return render(request, 'admin/subcatform.html', {'form': form})