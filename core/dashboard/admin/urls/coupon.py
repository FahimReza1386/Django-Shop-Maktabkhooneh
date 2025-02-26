from django.urls import path
from .. import views

urlpatterns = [
    path("order/coupons/list/", views.AdminOrderCouponsListView.as_view(), name="order-coupons-list"),
    path("order/coupon/create/", views.AdminOrderCouponCreateView.as_view(), name="order-coupon-create"),
    path("order/coupon/<int:pk>/update/", views.AdminOrderCouponUpdateView.as_view(), name="order-coupon-update"),
    path("order/coupon/<int:pk>/delete/", views.AdminOrderCouponDeleteView.as_view(), name="order-coupon-delete"),
    path("order/coupon/<int:pk>/used_by/list/", views.AdminOrderCouponUsed_ByListView.as_view(), name="order-coupon-used_by-list"),
]