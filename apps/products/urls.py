from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.all_products, name="all_products"),
    path("products/<int:p_id>/", views.product_details, name="product_details"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/<int:p_id>/update/", views.update_product, name="update_product"),
]
