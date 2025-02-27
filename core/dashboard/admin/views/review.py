from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from ..forms import ReviewForm
from review.models import ReviewModel
from django.core.exceptions import FieldError
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

class AdminReviewListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "Dashboard/admin/reviews/review-list.html"
    form_class = ReviewForm
    model = ReviewModel
    paginate_by = 10


    def get_paginate_by(self, queryset):
        
        valid_page_sizes = {12, 15, 18, 21, 24}

        page_size_param = self.request.GET.get('page_size')

        try:
            page_size = int(page_size_param)
            if page_size > 0 or page_size in valid_page_sizes:
                return page_size
            else:
                return self.paginate_by
        except:
            return self.paginate_by

    def get_queryset(self):
            queryset =ReviewModel.objects.all().order_by('-created_date')
            if search_q := self.request.GET.get("q"):
                queryset = queryset.filter(product__title__icontains=search_q)
            if category_id := self.request.GET.get("category_id"):
                queryset = queryset.filter(category__id=category_id)
            if order_by := self.request.GET.get("order_by"):
                try:
                    queryset = queryset.order_by(order_by)
                except FieldError:
                    messages.error(self.request , ("خطا در وارد کردن فیلد"))
            return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        return context
    
class AdminReviewEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = "Dashboard/admin/reviews/review-edit.html"
    form_class = ReviewForm
    model = ReviewModel
    success_message = "اطلاعات بررسی شما با موفقیت تغییر کرد ."
    
    def get_success_url(self):
        return reverse_lazy("dashboard:dash_admin:review-edit", kwargs={"pk":self.kwargs["pk"]})
