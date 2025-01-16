from django.shortcuts import render
from django.views.generic import TemplateView, View
from .cart import CartSession
from django.http import JsonResponse
# Create your views here.


class SessionAddProduct(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if product_id:
            cart.add_product(product_id)
        return JsonResponse({"cart":cart.get_cart_dict(), "total_quantity":cart.get_total_quantity()})


class SessionCartSummary(TemplateView):
    template_name = "Cart/cart-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = CartSession(self.request.session)
        context["cart_items"] = cart.get_cart_items()
        context["total_quantity"] = cart.get_total_quantity()
        context["total_payment_price"] = cart.get_total_payment_price()

        return context

    