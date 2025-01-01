from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from .models import ProductModel, ProductStatusType, ProductCategoryModel

# Create your views here.
class ShopProductGridView(ListView):
    template_name = "Shop/product-grid.html"
    model = ProductModel
    paginate_by = 9

    def get_queryset(self):
        queryset =ProductModel.objects.filter(status=ProductStatusType.publish.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)

        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)

        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)

        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context['categories'] = ProductCategoryModel.objects.all()
        return context


class ShopProductDetailView(DetailView):
    template_name = "Shop/product-detail.html"
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)