from django.contrib import admin
from .models import PaymentModel
# Register your models here.

@admin.register(PaymentModel)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ["authority_id", "ref_id", "response_json", "response_code", "status"]
