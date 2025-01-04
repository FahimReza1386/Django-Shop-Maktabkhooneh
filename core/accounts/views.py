from django.contrib.auth import views as auth_views
from .forms import AuthenticationsForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here.


class LoginView(auth_views.LoginView):
    template_name="Accounts/login.html"
    form_class = AuthenticationsForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass
    

class ResetPasswordView(auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = '/'



class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name="users/password_reset_complete.html"
    success_url='/accounts/login/'


