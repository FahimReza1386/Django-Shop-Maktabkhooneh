from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.permissions import HasCustomerAccessPermission
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from dashboard.customer.forms import CustomerPasswordChangeForm, CustomerProfileEditForm
from accounts.models import Profile
from django.contrib import messages
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