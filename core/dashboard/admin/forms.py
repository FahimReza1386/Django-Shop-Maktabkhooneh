from django.contrib.auth import forms as auth_forms
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from shop.models import ProductModel, ProductImageModel
from order.models import CouponModel

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

class AdminProductCreateForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ["category","title", "slug", "image", "brief_description", "description", "stock", "status", "price", "discount_percent"]
    
    def __init__(self, *args, **kwargs):
        super(AdminProductCreateForm, self).__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["class"] = "form-control is-valid"
        self.fields["category"].widget.attrs["class"] = "form-control is-valid"




# -----------------------------------ProductImage Form------------------------------------
class AdminProductImageAddForm(forms.ModelForm):
    class Meta:
        model= ProductImageModel
        fields = ["file"]
        


# ------------------------------OrderCoupons--------------------------------
 
class AdminOrderCouponsListForm(forms.ModelForm):
    class Meta:
        model = CouponModel
        fields = ["code", "discount_percent", "max_limit_usage", "used_by", "expiration_date"]
  
class AdminOrderCouponsForm(forms.ModelForm):
    class Meta:
        model = CouponModel
        fields = ["code", "discount_percent", "max_limit_usage", "used_by", "expiration_date"]

        def __init__(self, *args, **kwargs):
            super(AdminOrderCouponsForm, self).__init__(*args, **kwargs)
            self.fields["used_by"].widget.attrs["class"] = "form-control is-valid"


# ------------------------------OrderCoupons--------------------------------
class AdminOrderCouponCreateForm(forms.ModelForm):
    class Meta:
        model = CouponModel
        fields = ["code", "discount_percent", "max_limit_usage", "expiration_date"] 


class AdminOrderCouponUsed_byForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["user", "first_name", "last_name", "phone_number", "gender"]