from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_products, name="all_products"),
    path("<int:id>/", views.product_details, name="product_details"),
    path("add/", views.add_product, name="add_product"),
]
