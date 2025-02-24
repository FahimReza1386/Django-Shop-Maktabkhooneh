from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SubmitReviewForm
from .models import ReviewModel

# Create your views here.


class SubmitReviewView(LoginRequiredMixin,CreateView):
    http_method_names = "post"
    form_class = SubmitReviewForm
    model = ReviewModel

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        product = form.cleaned_data["product"]
        messages.success(self.request, "دیدگاه شما با موفقیت ثبت شد ، پس از بررسی نمایش داده خواهد شد .")
        return redirect(reverse_lazy("shop:product-detail", kwargs={"slug":product.slug}))
    
   
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.request.META.get("HTTP_REFERER"))
