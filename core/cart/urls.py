from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("session/add-product", views.SessionAddProductView.as_view(), name="session-add-product"),
    path("session/cart/summary/", views.SessionCartSummaryView.as_view(), name="session-cart-summary"),
    path("session/update-product-qty/", views.SessionUpdateProductQtyView.as_view(), name="session-update-product-qty"),
    path("session/delete-product/", views.SessionDeleteProductView.as_view(), name="session-delete-product"),
    path("session/delete-all-cart/", views.SessionDeleteAllCartView.as_view(), name="session-delete-all-cart"),
]