from django.urls import path, include

app_name = "dash_admin"

urlpatterns = [
    path("",include("dashboard.admin.urls.generals")),
    path("",include("dashboard.admin.urls.coupon")),
    path("",include("dashboard.admin.urls.product")),
    path("",include("dashboard.admin.urls.profile")),
    path("",include("dashboard.admin.urls.review")),
]