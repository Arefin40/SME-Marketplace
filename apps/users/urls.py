from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("profile", views.profile, name="profile"),
    path("become-merchant", views.become_merchant, name="become-merchant"),
    path("address-book", views.address_book, name="address-book"),
    path("address/add", views.add_address, name="add-address"),
    path("address/<int:id>/delete", views.delete_address, name="delete-address"),
    path("zones", views.zones, name="get-zones"),
    path("areas", views.areas, name="get-areas"),
    # Admin views
    path("manage-users", views.manage_user, name="manage-users"),
    path("users/<int:id>/update-role", views.update_role, name="update-role"),
    path("merchant-applications", views.manage_merchant_applications, name="merchant-applications"),
    path(
        "merchant-applications/<int:id>/update-status",
        views.update_application_status,
        name="update-application-status",
    ),
]
