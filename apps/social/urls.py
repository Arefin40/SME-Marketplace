from django.urls import path
from . import views


urlpatterns = [
    path("posts/create", views.create_post, name="create-post"),
    path("posts/<int:pk>/edit", views.edit_post, name="edit-post"),
]
