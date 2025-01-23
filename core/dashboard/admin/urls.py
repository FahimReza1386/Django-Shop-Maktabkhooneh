from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "dash_admin"

urlpatterns = [
    path("home/", views.AdminDashBoardHomeView.as_view(), name="home"),
    path("security/edit/", views.AdminSecurityEditView.as_view(), name="security-edit"),
    path("profile/edit/", views.AdminProfileEditView.as_view(), name="profile-edit"),
    path("profile/image/edit/", views.AdminProfileImageEditView.as_view(), name="profile-image-edit"),
]