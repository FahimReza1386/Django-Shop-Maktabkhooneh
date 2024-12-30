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
    model = ProductModel
    querysets=ProductModel.objects.filter(status=ProductStatusType.publish.value)
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        return context
