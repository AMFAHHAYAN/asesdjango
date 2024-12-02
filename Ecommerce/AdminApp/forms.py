from django import forms
from .models import Product, Category, Subcategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category','subcategory', 'stock_quantity', 'photo']
        labels = {
            'name': "Product Name", 
            'description': "Product Description", 
            'price': "Product Price", 
            'subcategory': "Product Subcategory",
            'stock_quantity': "Product Stock Quantity",
            'photo': "Product Image"
        }
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),  # Changed from TextInput
            'price': forms.NumberInput(attrs={"class": "form-control"}),
            'stock_quantity': forms.NumberInput(attrs={"class": "form-control"})  # Changed from TextInput
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': "Category Name", 
            'description': "Category Description", 
        }
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),  # Changed from TextInput
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'description', 'category']
        labels = {
            'name': "SubCategory Name", 
            'description': "SubCategory Description",
            'category': "Parent Category"  # Added label for category
        }
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),  # Changed from TextInput
            'category': forms.Select(attrs={"class": "form-control"}),
        }