from django.urls import path
from django.urls import include
from . import views


app_name="dashboard"

urlpatterns = [
    path("home/", views.DashBoardHomeView.as_view(), name="home"),

    path("admin/", include("dashboard.admin.urls")),
    path("customer/", include("dashboard.customer.urls")),
]