from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from dashboard.admin.forms import AdminPasswordChangeForm, AdminProfileEditForm, AdminProductEditForm
from django.contrib import messages
from accounts.models import Profile
from shop.models import ProductModel, ProductCategoryModel, ProductStatusType
from django.core.exceptions import FieldError
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
        return context
