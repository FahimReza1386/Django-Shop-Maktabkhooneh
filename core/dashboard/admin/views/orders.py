from django.shortcuts import redirect
from django.views.generic import UpdateView, ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.permissions import HasAdminAccessPermission
from django.urls import reverse_lazy
from dashboard.admin.forms import AdminOrderCouponsListForm, AdminOrderCouponCreateForm, AdminOrderCouponsForm, AdminOrderCouponUsed_byForm
from django.contrib import messages
from accounts.models import Profile
from django.core.exceptions import FieldError
from order.models import CouponModel, OrderModel
from accounts.models import User

# ---------------------------------------Product-Coupon-Views-----------------------------------------------

class AdminOrderCouponsListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    form_class = AdminOrderCouponsListForm
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