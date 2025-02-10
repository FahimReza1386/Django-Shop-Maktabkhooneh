from django.urls import path
from . import views

app_name = "order"
urlpatterns = [
    path("validation/coupon/", views.ValidationCouponView.as_view(), name="order-validation-coupon"),
    path("checkout/", views.OrderCheckOutView.as_view(), name="order-checkout"),
    path("completed/", views.OrderCompletedView.as_view(), name="order-completed"),
    path("failed/", views.OrderFailedView.as_view(), name="order-failed"),
]