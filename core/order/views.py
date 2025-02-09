from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .permissions import HasCustomerAccessPermission
from django.views.generic import FormView, TemplateView, View
from order.models import UserAddressModel, OrderModel, OrderItemModel, CouponModel
from django.http import JsonResponse
from cart.models import CartModel
from order.forms import CheckOutForm
from cart.cart import CartSession
from decimal import Decimal
from datetime import timezone
from django.utils import timezone
from payment.zarinpal_client import ZarinPalSandBox
from payment.models import PaymentModel, PaymentStatusTypeModel
# Create your views here.

class ValidationCouponView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, View):
    def post(self, request, *args, **kwargs):
        code= request.POST.get("code")
        user = self.request.user

        status_code = 200
        message = "کد تخفیف با موفقیت اعمال شد ."
        total_price = 0
        total_tax = 0

        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            return JsonResponse({"message":"کد تخفیف نامعتبر میباشد ."}, status=404)

        else:   

            if coupon.used_by.count() >= coupon.max_limit_usage:
                status_code, message = 403, "محدودیت در تعداد استفاده کاربران ."

            elif coupon.expiration_date and coupon.expiration_date < timezone.now():
                status_code, message = 403, "کد تخفیف منقضی شده است ."

            
            elif user in coupon.used_by.all():
                status_code, message = 403, "این کد تخفیف قبلا توسط شما استفاده  شده است ."

            else:
                cart = CartModel.objects.get(user=self.request.user)

                total_price = cart.calculate_total_price()
                total_price = round(total_price - (total_price * (Decimal(coupon.discount_percent)/100)))
                total_tax = round((total_price * 10) / 100)


        return JsonResponse({"message":message, "total_tax":total_tax, "total_price":total_price},status=status_code) 

    

class OrderCheckOutView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, FormView):
    template_name = "Order/order-checkout.html"
    form_class=CheckOutForm
    success_url = reverse_lazy("order:order-completed")

    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs



    def form_valid(self, form):
        user = self.request.user
        cleaned_data = form.cleaned_data
        address = cleaned_data['address_id']
        coupon = cleaned_data['coupon']

        cart = CartModel.objects.get(user=user)
        order = self.create_order(address)

        self.create_order_items(order, cart)
        self.clear_cart(cart)

        total_price = order.calculate_total_price()
        self.apply_coupon(coupon, order, user, total_price)
        order.save()
        print(order)
        return redirect(self.create_payment_url(order))

    def create_order(self, address):
        return OrderModel.objects.create(
            user=self.request.user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
        )
    
    def create_payment_url(self, order):
        zarinpal = ZarinPalSandBox()
        response = zarinpal.payment_request(amount=float(order.total_price))
        data  = response["data"]
        authority = data["authority"]

        payment_obj = PaymentModel.objects.create(
            authority_id =authority,
            amount=order.total_price,
        )
        order.payment = payment_obj
        order.save()
        return zarinpal.generate_payment_url(authority=authority)
    
    def create_order_items(self, order, cart):
        for item in cart.cart_items.all():
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

    def clear_cart(self, cart):
        cart.cart_items.all().delete()
        CartSession(self.request.session).clear()

    def apply_coupon(self, coupon, order, user, total_price):
        if coupon:
            discount_amount = round(
                (total_price * Decimal(coupon.discount_percent / 100)))
            total_price -= discount_amount
            
            order.coupon = coupon
            coupon.used_by.add(user)
            coupon.save()

        order.total_price = total_price

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