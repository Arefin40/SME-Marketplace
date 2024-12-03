from django.urls import path
from . import views


urlpatterns = [
    path("cart", views.cart, name="cart"),
    path("cart/clear", views.clear_cart, name="clear-cart"),
    path("products/<int:pk>/add-to-cart", views.add_to_cart, name="add-to-cart"),
    path("products/<int:pk>/decrement", views.decrement_quantity, name="decrement-quantity"),
    path("products/<int:pk>/remove-from-cart", views.remove_from_cart, name="remove-from-cart"),
    path("checkout", views.checkout, name="checkout"),
    path("place-order", views.place_order, name="place-order"),
    path("thankyou", views.thankyou, name="thankyou"),
]
