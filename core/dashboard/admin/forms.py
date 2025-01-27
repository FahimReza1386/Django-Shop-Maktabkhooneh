from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from shop.models import ProductModel

class AdminPasswordChangeForm(auth_forms.PasswordChangeForm):
    error_messages = {
        "password_mismatch": _("پسورد جدید و تکرار آن باید یکسان باشند ."),
        "password_incorrect": _(
            "پسورد فعلی شما اشتباه است اگر به یاد نمی اورید میتواند برای فراموش رمز عبور اقدام کنید."
        ),
    }

class AdminProfileEditForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields= ["first_name","last_name","phone_number","gender"]

class AdminProductEditForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ["category","title", "slug", "image", "brief_description", "description", "stock", "status", "price", "discount_percent"]

    def __init__(self, *args, **kwargs):
        super(AdminProductEditForm, self).__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["class"] = "form-control is-valid"
        self.fields["category"].widget.attrs["class"] = "form-control is-valid"