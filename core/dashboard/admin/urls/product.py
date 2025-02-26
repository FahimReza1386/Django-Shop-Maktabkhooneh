from django.urls import path
from .. import views

urlpatterns = [
    # Product Urls
    path("product/list/", views.AdminProductListView.as_view(), name="products-list"),
    path("product/create/", views.AdminProductCreateView.as_view(), name="product-create"),
    path("product/<int:pk>/edit/", views.AdminProductEditView.as_view(), name="product-edit"),
    path("product/<int:pk>/delete/", views.AdminProductDeleteView.as_view(), name="product-delete"),
    # Crud For ProductImage
    path("product/image/<int:pk>/add/", views.AdminProductImageAddView.as_view(), name="product-image-add"),
    path("product/image/<int:pk>/delete/", views.AdminProductImageDeleteView.as_view(), name="product-image-delete"),
]