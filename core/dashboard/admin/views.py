from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
# Create your views here.

class AdminDashBoardHomeView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView):
    template_name = "Dashboard/admin/home.html"