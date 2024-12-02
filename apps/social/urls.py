from django.urls import path
from . import views


urlpatterns = [
    path("posts/create", views.create_post, name="create-post"),
    path("posts/manage", views.manage_posts, name="manage-posts"),
    path("posts/<int:pk>/edit", views.edit_post, name="edit-post"),
    path("posts/<int:pk>/delete", views.delete_post, name="delete-post"),
    path("wishlist/<int:p_id>/toggle", views.toggle_product_in_wishlist, name="toggle-wishlist"),
]
