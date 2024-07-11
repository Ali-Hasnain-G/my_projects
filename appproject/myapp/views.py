from django.shortcuts import get_list_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product

class ProductListView(APIView):
    def get(self, request):
        products = get_list_or_404(Product)
        data = [
            {
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'created_at': product.created_at
            }
            for product in products
        ]
        return Response(data)
