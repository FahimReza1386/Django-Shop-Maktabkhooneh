from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .permissions import HasCustomerAccessPermission
from django.views.generic import FormView, TemplateView
from order.models import UserAddressModel
from cart.models import CartModel
from order.forms import CheckOutForm

# Create your views here.

class OrderCheckOutView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, FormView):
    template_name = "Order/order-checkout.html"
    form_class=CheckOutForm
    success_url = reverse_lazy("order:order-completed")

    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        address_id = cleaned_data["address_id"]
        print(address_id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        cart = CartModel.objects.get(user=self.request.user)
        context["addresses"] = UserAddressModel.objects.filter(user=self.request.user)
        total_price = cart.calculate_total_price()
        context["total_price"] = total_price
        context["total_tax"] = round((total_price * 10)/100)
        return context
    

class OrderCompletedView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, TemplateView):
    template_name = "Order/order-completed.html"