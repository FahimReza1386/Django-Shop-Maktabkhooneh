from django.urls import path, re_path  
from . import views  

app_name = "shop"  

urlpatterns = [  
    path("product/grid/", views.ShopProductGridView.as_view(), name="product-grid"),   
    re_path(r"product/(?P<slug>[\u0600-\u06FF\-a-zA-Z0-9_]+)/detail/", views.ShopProductDetailView.as_view(), name='product-detail'),  
    path("add-or-remove-favorites/", views.ShopAddOrRemoveFavoritesView.as_view(), name="add-or-remove-favorites"),

]