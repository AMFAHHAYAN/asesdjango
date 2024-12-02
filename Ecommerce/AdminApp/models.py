from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(
        max_length=100, 
        unique=True, 
    )
    description = models.TextField(
        blank=True, 
        null=True, 
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
class Subcategory(models.Model):

    name = models.CharField(
        max_length=100, 
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='subcategories'
    )
    description = models.TextField(
        blank=True, 
        null=True, 
    )
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    class Meta:
        unique_together = ('name', 'category')
        verbose_name_plural = "Subcategories"

class Product(models.Model):
    
    name = models.CharField(
        max_length=200, 
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='products'
    )
    subcategory = models.ForeignKey(
        Subcategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='products'
    )
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.FileField(upload_to='image/',blank=True,null=True)
    def __str__(self):
        return self.name
