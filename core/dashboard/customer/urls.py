from django.urls import path
from . import views


app_name = "dash_customer"

urlpatterns = [
    path("home/", views.CustomerDashBoardHomeView.as_view(), name="home"),
    path("security/edit/", views.CustomerSecurityEditView.as_view(), name="security-edit"),
    path("profile/edit/", views.CustomerProfileEditView.as_view(), name="profile-edit"),
    path("profile/image/edit/", views.CustomerProfileImageEditView.as_view(), name="profile-image-edit"),
]