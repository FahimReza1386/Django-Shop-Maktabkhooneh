from django.urls import path
from .. import views

urlpatterns = [
    path("home/", views.AdminDashBoardHomeView.as_view(), name="home"),
]