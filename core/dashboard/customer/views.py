from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView, ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.permissions import HasCustomerAccessPermission
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from dashboard.customer.forms import CustomerPasswordChangeForm, CustomerProfileEditForm, CustomerAddressForm
from accounts.models import Profile
from django.contrib import messages
from order.models import UserAddressModel
from django.core.exceptions import FieldError
# Create your views here.

class CustomerDashBoardHomeView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = "Dashboard/customer/home.html"



class CustomerSecurityEditView(LoginRequiredMixin, HasCustomerAccessPermission,SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "Dashboard/customer/profile/security-edit.html"
    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy("dashboard:dash_customer:security-edit")
    success_message = "بروزرسانی پسورد با موفقیت انجام شد ."


class CustomerProfileEditView(LoginRequiredMixin, HasCustomerAccessPermission,SuccessMessageMixin, UpdateView):
    template_name = "Dashboard/customer/profile/profile-edit.html"
    success_url = reverse_lazy("dashboard:dash_customer:profile-edit")
    form_class = CustomerProfileEditForm
    success_message = "بروزرسانی پروفایل با موفقیت انجام شد ."

    def get_object(self, queryset = None):

        return Profile.objects.get(user=self.request.user)
    

class CustomerProfileImageEditView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, UpdateView):
    model = Profile
    fields = ["image"]
    http_method_names = ["post"]
    success_url = reverse_lazy("dashboard:dash_customer:profile-edit")
    success_message = "بروزرسانی تصویر پروفایل با موفقیت انجام شد ."

    def get_object(self, queryset = None):

        return Profile.objects.get(user=self.request.user)
    
    def form_invalid(self, form):
        messages.error(self.request,"ارسال تصویر با مشکل مواجه شد . لطفا محددا بررسی و تلاش نمایید . ")
        return redirect(self.success_url)
    

# ------------------------------------Addresses Url-------------------------------------------
class CustomerAddressListView(LoginRequiredMixin, HasCustomerAccessPermission, ListView):
    model = UserAddressModel
    template_name = "Dashboard/customer/addresses/address-list.html"

    def get_queryset(self):
        queryset =UserAddressModel.objects.filter(user=self.request.user)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)

        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                messages.error(self.request , ("خطا در وارد کردن فیلد"))

        return queryset

class CustomerAddressEditView(LoginRequiredMixin, HasCustomerAccessPermission,SuccessMessageMixin, UpdateView):
    template_name = "Dashboard/customer/addresses/address-edit.html"
    form_class = CustomerAddressForm
    success_message = "بروزرسانی آدرس انتخابی شما با موفقیت انجام شد ."
    success_url = reverse_lazy("dashboard:dash_customer:address-list")
    def get_queryset(self):
        return UserAddressModel.objects.filter(pk=self.kwargs["pk"])
    
class CustomerAddressDeleteView(LoginRequiredMixin, HasCustomerAccessPermission,SuccessMessageMixin, DeleteView):
    success_message = "حذف آدرس انتخابی شمابا موفقیت انجام شد ."
    success_url = reverse_lazy("dashboard:dash_customer:address-list")
    http_method_names = "post"

    def get_queryset(self):
        queryset = UserAddressModel.objects.filter(pk=self.kwargs["pk"])
        return queryset

class CustomerAddressCreateView(LoginRequiredMixin, HasCustomerAccessPermission, CreateView):
    model = UserAddressModel
    template_name = "Dashboard/customer/addresses/address-add.html"
    form_class = CustomerAddressForm
    success_url = reverse_lazy("dashboard:dash_customer:address-list")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
