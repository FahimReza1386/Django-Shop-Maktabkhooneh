from django.urls import path
from . import views

app_name="shop"

urlpatterns =[
    path("product/grid/" , views.ShopProductGrid.as_view(), name="product-grid"),   
    # path("product/list/" , views.ShopProductGrid.as_view(), name="product-list"),   
]