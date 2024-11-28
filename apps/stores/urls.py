from django.urls import path
from . import views


urlpatterns = [
    path("store", views.view_store, name="storeUser"),
    path("stores/create", views.create_store, name="create-store"),
    path("manage-inventory", views.manage_inventory, name="manage-inventory"),
    path("manage-orders", views.manage_orders, name="manage-orders"),
]
