from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
]

from django.http import JsonResponse
from .models import Product

def product_list(request):
    # Dummy data (you would normally query the database here)
    products = [
        {"title": "Product 1", "description": "Description 1", "price": "10.00"},
        {"title": "Product 2", "description": "Description 2", "price": "20.00"},
    ]
    
    return JsonResponse(products, safe=False)

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from django.utils import timezone

@receiver(post_save, sender=Product)
def update_created_at(sender, instance, created, **kwargs):
    if created:
        instance.created_at = timezone.now()
        instance.save()
INSTALLED_APPS = [
    'myapp',
]
