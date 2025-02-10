from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import PaymentModel, PaymentStatusTypeModel
from .zarinpal_client import ZarinPalSandBox
from order.models import OrderModel, OrderStatusType

# Create your views here.


class PaymentVerifyView(View):
    def get(self, request, *args, **kwargs):
        authority_id= request.GET.get("Authority")
        status= request.GET.get("Status")
        payment_obj = get_object_or_404(PaymentModel, authority_id=authority_id)
        order = OrderModel.objects.get(payment = payment_obj)
        zarinpal = ZarinPalSandBox()
        response =zarinpal.payment_verify(int(payment_obj.amount), payment_obj.authority_id)
        data = response["data"]
        if data:
            if data["code"] == 100 or data["code"] == 101:
                payment_obj.ref_id = data["ref_id"]
                payment_obj.response_code = data["code"]
                payment_obj.status = PaymentStatusTypeModel.success.value
                payment_obj.response_json = response
                payment_obj.save()
                order.status = OrderStatusType.processing.value
                order.save()
                return redirect(reverse_lazy("order:order-completed"))
        else : 
            payment_obj.status = PaymentStatusTypeModel.failed.value
            payment_obj.response_json = response
            payment_obj.save()
            order.status = OrderStatusType.canceled.value
            order.save()

            return redirect(reverse_lazy("order:order-failed"))
    