from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    View,
)
from django.core.exceptions import FieldError
from .models import ProductModel, ProductStatusType, ProductCategoryModel, ProductImageModel, FavoritesProductModel
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from accounts.models import User
# Create your views here.
class ShopProductGridView(ListView):
    template_name = "Shop/product-grid.html"
    model = ProductModel
    paginate_by = 9


    def get_paginate_by(self, queryset):
        
        valid_page_sizes = {12, 15, 18, 21, 24}

        page_size_param = self.request.GET.get('page_size')

        try:
            page_size = int(page_size_param)
            if page_size > 0 or page_size in valid_page_sizes:
                return page_size
            else:
                return self.paginate_by
        except:
            return self.paginate_by

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
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                messages.error(self.request , ("خطا در وارد کردن فیلد"))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context['categories'] = ProductCategoryModel.objects.all()
        context['Favorites_product'] = FavoritesProductModel.objects.filter(user=self.request.user).values_list('product__id', flat=True)  if self.request.user.is_authenticated else []
        return context


class ShopProductDetailView(DetailView):
    template_name = "Shop/product-detail.html"
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_picture"] = ProductImageModel.objects.all()
        context['Favorites_product'] = FavoritesProductModel.objects.filter(user=self.request.user).values_list('product__id', flat=True)  if self.request.user.is_authenticated else []

        return context
    

class ShopAddOrRemoveFavoritesView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        message = ""
        product_id = request.POST.get("product_id")
        user = request.user
        if product_id:
            try:
                obj = FavoritesProductModel.objects.get(user=user, product__id=product_id)
                obj.delete()
                message = "محصول انتخابی با موفقیت از لیست علاقه مندی ها حذف شد ."
                messages.success(request, "محصول انتخابی با موفقیت از لیست علاقه مندی ها حذف شد .")


            except FavoritesProductModel.DoesNotExist:
                product = ProductModel.objects.get(id=product_id)
                FavoritesProductModel.objects.create(user=user, product=product)
                message = "محصول انتخابی با موفقیت به لیست علاقه مندی ها اضافه شد ."
                messages.success(request, "محصول انتخابی با موفقیت به لیست علاقه مندی ها اضافه شد .")

        return JsonResponse({"message":message})