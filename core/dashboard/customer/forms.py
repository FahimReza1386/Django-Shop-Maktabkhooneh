from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from order.models import UserAddressModel, OrderModel

class CustomerPasswordChangeForm(auth_forms.PasswordChangeForm):
    error_messages = {
        "password_mismatch": _("پسورد جدید و تکرار آن باید یکسان باشند ."),
        "password_incorrect": _(
            "پسورد فعلی شما اشتباه است اگر به یاد نمی اورید میتواند برای فراموش رمز عبور اقدام کنید."
        ),
    }

class CustomerProfileEditForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields= ["first_name","last_name","phone_number","gender"]



class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model= UserAddressModel
        fields = ["address", "state", "city", "zip_code"]

    def __init__(self, *args, **kwargs):
        super(CustomerAddressForm, self).__init__(*args, **kwargs)
        self.fields["address"].widget.attrs["class"] = "form-control is-valid text-center"
        self.fields["state"].widget.attrs["class"] = "form-control is-valid text-center"
        self.fields["city"].widget.attrs["class"] = "form-control is-valid text-center"
        self.fields["zip_code"].widget.attrs["class"] = "form-control is-valid text-center"


class CustomerOrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ["total_price", "coupon", "status", "address", "state", "city", "zip_code"]