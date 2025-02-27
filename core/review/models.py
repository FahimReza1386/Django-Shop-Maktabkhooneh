from django.db import models
from shop.models import ProductModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models import Avg
# Create your models here.

class ReviewStatusType(models.IntegerChoices):
    pending = 1, "در انتظار تایید خرید"
    accepted = 2, "خرید تایید شده"
    rejected = 3, "خرید رد شده"

class ReviewModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT)
    description = models.CharField()
    rate = models.IntegerField(default=5, validators=[MinValueValidator(0),MaxValueValidator(5)])
    status = models.IntegerField(choices=ReviewStatusType.choices, default=ReviewStatusType.pending.value)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    
def update_product_average_rate(product):
    approved_reviews = ReviewModel.objects.filter(product=product, status=ReviewStatusType.accepted.value)
    if approved_reviews.exists():
        average_rate = approved_reviews.aggregate(Avg('rate'))['rate__avg']
        product.avg_rate = round(average_rate, 1)
    else:
        product.avg_rate = 0
    product.save()



@receiver(post_save, sender=ReviewModel)
def review_post_save(sender, instance, **kwargs):
    if instance.status == ReviewStatusType.accepted.value or ReviewStatusType.rejected.value:
        update_product_average_rate(instance.product)

@receiver(post_delete, sender=ReviewModel)
def review_post_delete(sender, instance, **kwargs):
    if instance.status == ReviewStatusType.rejected.value:
        update_product_average_rate(instance.product)
