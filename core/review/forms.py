from django import forms
from .models import ReviewModel
from shop.models import ProductModel, ProductStatusType

class SubmitReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ["product", "description", "rate"]
        error_messages = {
            'description' : {
                'required' : 'فیلد توضیحات اجباری است .'
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")

        try:
            ProductModel.objects.get(id=product.id, status=ProductStatusType.publish.value)
        except ProductModel.DoesNotExist:
            return forms.ValidationError("The product you selected is not defined.")
        
        return cleaned_data
