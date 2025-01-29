from django.shortcuts import render
from django.views.generic import TemplateView, View, UpdateView, DeleteView
from .cart import CartSession
from django.http import JsonResponse
# Create your views here.


class SessionAddProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        qty = request.POST.get("quantity")
        if product_id and qty:
            cart.add_product(product_id,qty)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart":cart.get_cart_dict(), "total_quantity":cart.get_total_quantity()})


class SessionCartSummaryView(TemplateView):
    template_name = "Cart/cart-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = CartSession(self.request.session)
        context["cart_items"] = cart.get_cart_items()
        context["total_quantity"] = cart.get_total_quantity()
        context["total_payment_price"] = cart.get_total_payment_price()

        return context

    

class SessionUpdateProductQtyView(UpdateView):
    
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        if product_id and quantity:
            cart.update_product_qty(product_id, quantity)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        return JsonResponse({"cart":cart.get_cart_dict(), "total_quantity":cart.get_total_quantity()})


class SessionDeleteProductView(DeleteView):
   
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if product_id:
            cart.delete_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)

        return JsonResponse({"cart":cart.get_cart_dict(), "total_quantity":cart.get_total_quantity()})
 


class SessionDeleteAllCartView(DeleteView):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        cart.clear() 
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)   
        return JsonResponse({"cart":cart.get_cart_dict(), "total_quantity":cart.get_total_quantity()})
 