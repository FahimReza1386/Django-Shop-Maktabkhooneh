from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class ShopProductGrid(TemplateView):
    template_name = "Shop/product-grid.html"