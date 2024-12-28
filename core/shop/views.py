from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from .models import ProductModel, ProductStatusType

# Create your views here.

class ShopProductGrid(ListView):
    template_name = "Shop/product-grid.html"
    querysets= ProductModel.objects.filter(status=ProductStatusType.publish.value)