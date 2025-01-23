from django.shortcuts import redirect
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from dashboard.admin.forms import AdminPasswordChangeForm, AdminProfileEditForm
from accounts.models import Profile
# Create your views here.

class AdminDashBoardHomeView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView):
    template_name = "Dashboard/admin/home.html"

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