from django.shortcuts import render
from django.views import View
from .cart import CartSession
# Create your views here.


class SessionAddProduct(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        return {"cart":cart.get_cart_items()}
