from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"
urlpatterns= [
    path("login/", views.LoginView.as_view() , name="login"),
    path("logout/", views.LogoutView.as_view() , name="logout"),
    path("reset_password/", views.ResetPasswordView.as_view() , name="reset_password"),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',success_url='/accounts/password-reset-complete/'),
        name='password_reset_confirm'),

    path('password-reset-complete/',views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]