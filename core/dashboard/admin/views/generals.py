from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission

# ------------------------------General View--------------------------------------

class AdminDashBoardHomeView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView):
    template_name = "Dashboard/admin/home.html"
