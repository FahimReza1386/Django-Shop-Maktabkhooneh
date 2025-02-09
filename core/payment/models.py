from django.db import models
from django.db.models import JSONField
# Create your models here.

class PaymentStatusTypeModel(models.IntegerChoices):
    pending = 1, "در انتطار"
    success = 2, "پرداخت موفق"
    failed = 3, "پرداخت نا موفق"

class PaymentModel(models.Model):
    authority_id = models.CharField(max_length=255)
    ref_id = models.BigIntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, default=0, decimal_places=0)
    response_json = JSONField(default=dict)
    response_code = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(choices = PaymentStatusTypeModel.choices, default=PaymentStatusTypeModel.pending.value)

