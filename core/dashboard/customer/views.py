from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
# Create your views here.

class CustomerDashBoardHomeView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = "Dashboard/customer/home.html"