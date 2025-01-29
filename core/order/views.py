from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .permissions import HasCustomerAccessPermission
from django.views.generic import TemplateView

# Create your views here.

class OrderCheckOutView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, TemplateView):
    template_name = "Order/checkout.html"