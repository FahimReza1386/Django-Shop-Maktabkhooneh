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
    path("profile/list/", views.AdminProductListView.as_view(), name="products-list"),
    path("profile/<int:pk>/edit/", views.AdminProductEditView.as_view(), name="product-edit"),
    path("profile/<int:pk>/delete/", views.AdminProductDeleteView.as_view(), name="product-delete"),
]