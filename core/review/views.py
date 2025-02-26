from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SubmitReviewForm
from .models import ReviewModel, ReviewStatusType
from order.models import OrderModel, OrderItemModel, OrderStatusType

# Create your views here.


class SubmitReviewView(LoginRequiredMixin,CreateView):
    http_method_names = "post"
    form_class = SubmitReviewForm
    model = ReviewModel

    def form_valid(self, form):
        product = form.cleaned_data["product"]
        orders = OrderModel.objects.filter(user=self.request.user, status=OrderStatusType.delivered.value)
        order = list(orders)
        is_buy = OrderItemModel.objects.filter(order__in=order, product=product).exists()
        if is_buy != True:
            form.instance.status = ReviewStatusType.rejected.value
        else :
            form.instance.status = ReviewStatusType.accepted.value
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, "دیدگاه شما با موفقیت ثبت شد ، پس از بررسی نمایش داده خواهد شد .")
        return redirect(reverse_lazy("shop:product-detail", kwargs={"slug":product.slug}))
    
   
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.request.META.get("HTTP_REFERER"))

    
