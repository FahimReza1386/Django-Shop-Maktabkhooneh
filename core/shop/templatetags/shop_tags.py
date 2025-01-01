from django import template
from shop.models import ProductModel, ProductStatusType

register = template.Library()

@register.inclusion_tag("includes/latest_products.html")
def show_latest_products():
    latest_product = ProductModel.objects.filter(status=ProductStatusType.publish.value).order_by("-created_date")[:8]
    return {"latest_products":latest_product}


@register.inclusion_tag("includes/similar_products.html")
def show_similar_products(product):
    category_product = product.category.all()
    latest_product = ProductModel.objects.filter(status=ProductStatusType.publish.value, category__in=category_product).order_by("-created_date")[:4]
    return {"similar_products":latest_product}