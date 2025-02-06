from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "dash_admin"

urlpatterns = [
    # General Urls
    path("home/", views.AdminDashBoardHomeView.as_view(), name="home"),
    # Profile Urls
    path("security/edit/", views.AdminSecurityEditView.as_view(), name="security-edit"),
    path("profile/edit/", views.AdminProfileEditView.as_view(), name="profile-edit"),
    path("profile/image/edit/", views.AdminProfileImageEditView.as_view(), name="profile-image-edit"),
    # Product Urls
    path("product/list/", views.AdminProductListView.as_view(), name="products-list"),
    path("product/create/", views.AdminProductCreateView.as_view(), name="product-create"),
    path("product/<int:pk>/edit/", views.AdminProductEditView.as_view(), name="product-edit"),
    path("product/<int:pk>/delete/", views.AdminProductDeleteView.as_view(), name="product-delete"),
    # Crud For ProductImage
    path("product/image/<int:pk>/add/", views.AdminProductImageAddView.as_view(), name="product-image-add"),
    path("product/image/<int:pk>/delete/", views.AdminProductImageDeleteView.as_view(), name="product-image-delete"),
    # Crun For CouponModel
    path("order/coupons/list/", views.AdminOrderCouponsListView.as_view(), name="order-coupons-list"),
    path("order/coupon/create/", views.AdminOrderCouponCreate.as_view(), name="order-coupon-create"),
    # path("order/coupon/update/", views.AdminOrderCouponUpdate.as_view(), name="order-update-coupon"),
    # path("order/coupon/delete/", views.AdminOrderCouponDelete.as_view(), name="order-delete-coupon"),
    
]