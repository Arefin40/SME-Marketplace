from django.urls import path
from . import views


urlpatterns = [
    path("stores/create", views.create_store, name="create-store"),
    path("stores/<slug:slug>", views.store, name="store"),
    path("stores/<slug:slug>/follow", views.toggle_follow_store, name="toggle-follow-store"),
    path("manage-inventory", views.manage_inventory, name="manage-inventory"),
    path("manage-orders", views.manage_orders, name="manage-orders"),
    path("wishlist", views.wishlist, name="wishlist"),
]
