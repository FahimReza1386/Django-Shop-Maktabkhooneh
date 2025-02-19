from django.urls import path
from . import views


app_name = "dash_customer"

urlpatterns = [
    path("home/", views.CustomerDashBoardHomeView.as_view(), name="home"),
    path("security/edit/", views.CustomerSecurityEditView.as_view(), name="security-edit"),
    path("profile/edit/", views.CustomerProfileEditView.as_view(), name="profile-edit"),
    path("profile/image/edit/", views.CustomerProfileImageEditView.as_view(), name="profile-image-edit"),

    # Addresses Url
    path("address/list/", views.CustomerAddressListView.as_view(), name="address-list"),
    path("address/<int:pk>/edit/", views.CustomerAddressEditView.as_view(), name="address-edit"),
    path("address/<int:pk>/delete/", views.CustomerAddressDeleteView.as_view(), name="address-delete"),
    path("address/create/", views.CustomerAddressCreateView.as_view(), name="address-create"),

    # Order Urls
    path("order/list/", views.CustomerOrderListView.as_view(), name="order-list"),
    path("order/<int:pk>/detail/", views.CustomerOrderDetailView.as_view(), name="order-detail"),
    path("order/<int:pk>/invoice/", views.CustomerOrderInvoiceView.as_view(), name="order-invoice"),

    # Favorites urls
    path("favorites/list/", views.CustomerFavoritesListView.as_view(), name="favorites-list"),
    path("favorites/<int:pk>/delete/", views.CustomerFavoritesDeleteView.as_view(), name="favorites-delete"),



]