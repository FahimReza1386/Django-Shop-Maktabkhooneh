from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.permissions import HasAdminAccessPermission
from django.urls import reverse_lazy
from dashboard.admin.forms import AdminProductEditForm, AdminProductCreateForm, AdminProductImageAddForm, AdminOrderCouponsListForm, AdminOrderCouponCreateForm, AdminOrderCouponsForm, AdminOrderCouponUsed_byForm
from django.contrib import messages
from shop.models import ProductModel, ProductCategoryModel, ProductImageModel
from django.core.exceptions import FieldError

# ------------------------------Product View--------------------------------------

class AdminProductListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name="Dashboard/admin/products/products-list.html"
    model = ProductModel
    paginate_by = 10


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
        queryset =ProductModel.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
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
        return context


class AdminProductCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    model=ProductModel
    success_url = reverse_lazy("dashboard:dash_admin:products-list")
    success_message = "ایجاد مخصول جدید شما با موفقیت انجام شد ."
    form_class = AdminProductCreateForm
    template_name = "Dashboard/admin/products/product-create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AdminProductEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name="Dashboard/admin/products/product-edit.html"
    queryset = ProductModel.objects.all()
    form_class = AdminProductEditForm
    success_message="بروزرسانی محصول با موفقیت انجام شد ."

    def get_success_url(self):
        return reverse_lazy("dashboard:dash_admin:products-list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategoryModel.objects.all()
        context['extra_picture'] = ProductImageModel.objects.all()
        return context


class AdminProductDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("dashboard:dash_admin:products-list")
    success_message = "حذف محصول مورد نظر با موفقیت انجام شد ."
    model = ProductModel 
    http_method_names = ["post"]


#  ---------------------------------- Product Image View-------------------------------------

class AdminProductImageAddView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, CreateView):
    model = ProductImageModel
    success_url = reverse_lazy("dashboard:dash_admin:products-list")
    success_message = "افزودن تصویر جدید به محصول مورد نظر با موفقیت انجام شد ."
    template_name = "Dashboard/admin/products/product-image-add.html"
    form_class = AdminProductImageAddForm


    def get_object(self):

        return get_object_or_404(ProductModel, pk=self.kwargs['pk'])


    def form_valid(self, form):
        form.instance.product = self.get_object()
        return super().form_valid(form)
    


class AdminProductImageDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    success_message = "حذف تصویر محصول مورد نظر با موفقیت انجام شد ."
    model = ProductImageModel
    http_method_names = ["post"]

    def get_object(self):
        return ProductImageModel.objects.get(id = self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy("dashboard:dash_admin:product-edit", kwargs={"pk":self.get_object().product.pk})

