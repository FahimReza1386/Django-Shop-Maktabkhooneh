from django import forms 
from order.models import UserAddressModel, CouponModel
from datetime import timezone
class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True)
    coupon = forms.CharField(required=False)


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request',None)
        super(CheckOutForm, self).__init__(*args, **kwargs)


    def clean_address_id(self):
        address_id = self.cleaned_data.get("address_id")

        user = self.request.user

        try:
            address= UserAddressModel.objects.get(id=address_id, user=user)
        except UserAddressModel.DoesNotExist:
            raise forms.ValidationError("Invalid address for the requested user .")
        
        return address

    def clean_coupon(self):
        code = self.cleaned_data.get("coupon")
        if code == "":
            return None

        user = self.request.user

        coupon= None

        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            raise forms.ValidationError("کد تخفیف شما نامعتبر است .")
        
        if coupon:

                if coupon.used_by.count() >= coupon.max_limit_usage:
                    raise forms.ValidationError("محدودیت در تعداد استفاده کاربران ...")

                if coupon.expiration_date and coupon.expiration_date < timezone.now():
                    raise forms.ValidationError("کد تخفیف منقضی شده است ...")
                
                if user in coupon.used_by.all():
                    raise forms.ValidationError("این کد تخفیف قبلا توسط شما استفاده شده است .. ")

        return coupon   