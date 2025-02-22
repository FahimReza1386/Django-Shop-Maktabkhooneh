from django import template
from shop.models import ProductModel, ProductStatusType, FavoritesProductModel

register = template.Library()

@register.inclusion_tag("includes/latest_products.html", takes_context=True)
def show_latest_products(context):
    request = context.get("request")
    latest_product = ProductModel.objects.filter(status=ProductStatusType.publish.value).distinct().order_by("-created_date")[:8]
    Favorites_product = FavoritesProductModel.objects.filter(user=request.user).values_list('product__id', flat=True)
    return {"latest_products":latest_product, "request":request , "Favorites_product":Favorites_product}


@register.inclusion_tag("includes/similar_products.html", takes_context=True)
def show_similar_products(context,product):
    request = context.get("request")
    category_product = product.category.all()
    latest_product = ProductModel.objects.filter(status=ProductStatusType.publish.value, category__in=category_product).distinct().order_by("-created_date")[:4]
    Favorites_product = FavoritesProductModel.objects.filter(user=request.user).values_list('product__id', flat=True)

    return {"similar_products":latest_product, "request":request, "Favorites_product":Favorites_product}