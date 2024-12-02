from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Product, Category, Subcategory
from .forms import ProductForm, CategoryForm, SubcategoryForm

class AdminLoginRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)
    
    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect('adminlogin')

class AdminLogin(View):
    def get(self, request):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return redirect('dashboard')
        return render(request, 'admin/adminlogin.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pass')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials or insufficient permissions.")
            return render(request, 'admin/adminlogin.html')

class AdminLogout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Successfully logged out.")
        return redirect('/')

class DashboardView(AdminLoginRequiredMixin, View):
    def get(self, request):
        context = {
            'total_products': Product.objects.count(),
            'total_categories': Category.objects.count(),
            'total_subcategories': Subcategory.objects.count()
        }
        return render(request, 'admin/dashboard.html', context)

class ProductListView(AdminLoginRequiredMixin, View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        
       
        product_list = Product.objects.all()
        if search_query:
            product_list = product_list.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        
      
        paginator = Paginator(product_list, 1)  
        page = request.GET.get('page', 1)
        
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        
        context = {
            'products': products, 
            'search_query': search_query
        }
        return render(request, 'admin/prodlist.html', context)

class ProductFormView(AdminLoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            form = ProductForm(instance=product)
        else:
            form = ProductForm()
        return render(request, 'admin/product-form.html', {'form': form})
    
    def post(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            form = ProductForm(request.POST, request.FILES, instance=product)
        else:
            form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Product saved successfully.")
            return redirect('product_list')
        else:
            messages.error(request, "Please correct the errors in the form.")
            return render(request, 'admin/product-form.html', {'form': form})

class ProductDeleteView(AdminLoginRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('product_list')

class CategoryListView(AdminLoginRequiredMixin, View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        
        category_list = Category.objects.all()
        if search_query:
            category_list = category_list.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        paginator = Paginator(category_list, 2)
        page = request.GET.get('page', 1)
        
        try:
            categories = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            categories = paginator.page(1)
        
        context = {
            'categories': categories, 
            'search_query': search_query
        }
        return render(request, 'admin/categorylist.html', context)


class CategoryFormView(AdminLoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            category = get_object_or_404(Category, pk=pk)
            form = CategoryForm(instance=category)
        else:
            form = CategoryForm()
        return render(request, 'admin/categoryform.html', {'form': form})
    
    def post(self, request, pk=None):
        if pk:
            category = get_object_or_404(Category, pk=pk)
            form = CategoryForm(request.POST, instance=category)
        else:
            form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Category saved successfully.")
            return redirect('catoglist')
        else:
            messages.error(request, "Please correct the errors in the form.")
            return render(request, 'admin/categoryform.html', {'form': form})

class CategoryDeleteView(AdminLoginRequiredMixin, View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('catoglist')

class SubcategoryListView(AdminLoginRequiredMixin, View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        
        subcategory_list = Subcategory.objects.all()
        if search_query:
            subcategory_list = subcategory_list.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        
        paginator = Paginator(subcategory_list, 2)
        page = request.GET.get('page', 1)
        
        try:
            subcategories = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            subcategories = paginator.page(1)
        
        context = {
            'subcategories': subcategories, 
            'search_query': search_query
        }
        return render(request, 'admin/subcategries.html', context)

class SubcategoryFormView(AdminLoginRequiredMixin, View):
    def get(self, request, pk=None):
        if pk:
            subcategory = get_object_or_404(Subcategory, pk=pk)
            form = SubcategoryForm(instance=subcategory)
        else:
            form = SubcategoryForm()
        return render(request, 'admin/subcatform.html', {'form': form})
    
    def post(self, request, pk=None):
        if pk:
            subcategory = get_object_or_404(Subcategory, pk=pk)
            form = SubcategoryForm(request.POST, instance=subcategory)
        else:
            form = SubcategoryForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Subcategory saved successfully.")
            return redirect('subcatlist')
        else:
            messages.error(request, "Please correct the errors in the form.")
            return render(request, 'admin/subcatform.html', {'form': form})

class SubcategoryDeleteView(AdminLoginRequiredMixin, View):
    def get(self, request, pk):
        subcategory = get_object_or_404(Subcategory, pk=pk)
        subcategory.delete()
        messages.success(request, "Subcategory deleted successfully.")
        return redirect('subcatlist')
    
class Landing(View):
    def get(self,request):
        return render(request,'landing.html')