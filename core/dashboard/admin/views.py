from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView, ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from dashboard.admin.forms import AdminPasswordChangeForm, AdminProfileEditForm, AdminProductEditForm, AdminProductCreateForm, AdminProductImageAddForm, AdminOrderCouponsForm, AdminOrderCouponCreateForm, AdminOrderCouponUsed_byForm
from django.contrib import messages
from accounts.models import Profile
from shop.models import ProductModel, ProductCategoryModel, ProductImageModel
from django.core.exceptions import FieldError
from order.models import CouponModel, OrderModel
from accounts.models import User
import jdatetime

# Create your views here.

# ------------------------------General View--------------------------------------

class AdminDashBoardHomeView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView):
    template_name = "Dashboard/admin/home.html"

# ------------------------------Profile View--------------------------------------

class AdminSecurityEditView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "Dashboard/admin/profile/security-edit.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:dash_admin:security-edit")
    success_message = "بروزرسانی پسورد با موفقیت انجام شد ."


class AdminProfileEditView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, UpdateView):
    template_name = "Dashboard/admin/profile/profile-edit.html"
    success_url = reverse_lazy("dashboard:dash_admin:profile-edit")
    form_class = AdminProfileEditForm
    success_message = "بروزرسانی پروفایل با موفقیت انجام شد ."

    def get_object(self, queryset = None):

        return Profile.objects.get(user=self.request.user)
    

class AdminProfileImageEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    model = Profile
    fields = ["image"]
    http_method_names = ["post"]
    success_url = reverse_lazy("dashboard:dash_admin:profile-edit")
    success_message = "بروزرسانی تصویر پروفایل با موفقیت انجام شد ."

    def get_object(self, queryset = None):

        return Profile.objects.get(user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(self.request,"ارسال تصویر با مشکل مواجه شد . لطفا محددا بررسی و تلاش نمایید . ")
        return redirect(self.success_url)
    



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



# ---------------------------------------Product-Coupon-Views-----------------------------------------------

class AdminOrderCouponsListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    form_class = AdminOrderCouponsForm
    template_name = "Dashboard/admin/order/coupons/coupons-list.html"
    queryset = CouponModel.objects.all().order_by("-created_date")
    paginate_by = 5

    def get_paginate_by(self, queryset):
            valid_page_sizes = {5, 10, 15, 20}
            page_size_param = self.request.GET.get('page_size')

            try:
                page_size = int(page_size_param)
                if page_size > 0 or page_size in valid_page_sizes:
                    return page_size
                else:
                    return self.paginate_by
            except:
                return self.paginate_by

    def  get_queryset(self):
        queryset = CouponModel.objects.all().order_by("-created_date")
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title_icontains = search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                messages.error(self.request , ("خطا در وارد کردن فیلد"))
        return queryset


class AdminOrderCouponCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    template_name = "Dashboard/admin/order/coupons/coupon-create.html"
    form_class = AdminOrderCouponCreateForm
    success_message = "کد تخفیف شما با موفقیت ایجاد شد ."
    success_url = reverse_lazy("dashboard:dash_admin:order-coupons-list")

    def form_valid(self, form):
        coupons = CouponModel.objects.all()
        for coupon in coupons:
            if coupon.code == form.instance.code:   
                messages.error(self.request, "سلام ادمین گرامی . کد شما قبلا تعریف شده .")
                return redirect(reverse_lazy("dashboard:dash_admin:order-coupon-create"))
        return super().form_valid(form)

class AdminOrderCouponUpdateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = "Dashboard/admin/order/coupons/coupon-update.html"
    form_class = AdminOrderCouponsForm
    success_message = "کد تخفیف شما با موفقیت بروزرسانی شد ."
    success_url = reverse_lazy("dashboard:dash_admin:order-coupons-list")
    queryset = CouponModel.objects.all()

class AdminOrderCouponDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    http_method_names = ["post"]
    success_message = "کد تخفیف شما با موفقیت حذف شد ."
    success_url = reverse_lazy("dashboard:dash_admin:order-coupons-list")
    model = CouponModel
   
    def form_valid(self, form):
        orders = OrderModel.objects.filter(coupon=self.object)
        if orders.exists():  # استفاده از self.object به جای form.instance
            messages.error(self.request, "سلام ادمین گرامی . کد شما قبلا استفاده شده عملیات حذف این موارد تنها توسط بخش امنیت انجام میشود . .")
            return redirect(reverse_lazy("dashboard:dash_admin:order-coupons-list"))
        return super().form_valid(form)
    

class AdminOrderCouponUsed_ByListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "Dashboard/admin/order/coupons/coupon-used_by.html"
    form_class = AdminOrderCouponUsed_byForm
    model = CouponModel
    paginate_by = 10

    def get_queryset(self):
        user = User.objects.all()
        test = CouponModel.objects.filter(id=self.kwargs["pk"], used_by__in=user)
        queryset = Profile.objects.none()

        for item in test:
            used_by = item.used_by.all()
            queryset = queryset | Profile.objects.filter(user__in=used_by)
        return queryset


    def get_paginate_by(self, queryset):
            valid_page_sizes = {5, 10, 15, 20}
            page_size_param = self.request.GET.get('page_size')

            try:
                page_size = int(page_size_param)
                if page_size > 0 or page_size in valid_page_sizes:
                    return page_size
                else:
                    return self.paginate_by
            except:
                return self.paginate_by
