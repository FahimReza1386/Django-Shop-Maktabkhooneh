from django.db import models
from shop.models import ProductModel
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class ReviewStatusType(models.IntegerChoices):
    pending = 1, "در انتظار تایید"
    accepted = 2, "تایید شده"
    rejected = 3, "رد شده"

class ReviewModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT)
    description = models.CharField()
    rate = models.IntegerField(default=5, validators=[MinValueValidator(0),MaxValueValidator(5)])
    status = models.IntegerField(choices=ReviewStatusType.choices, default=ReviewStatusType.pending.value)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)