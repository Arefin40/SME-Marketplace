from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.homepage, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # Include allauth URLs
    path("accounts/", include("allauth.urls")),
    # == Include the app's URLs ===
    path("", include("apps.users.urls")),
    path("", include("apps.stores.urls")),
    # For development only
    path("__reload__/", include("django_browser_reload.urls")),
    path("", include("apps.products.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
