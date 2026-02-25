from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/applications/", include("apps.applications.urls")),
    path("api/v1/dashboard/", include("apps.dashboard.urls")),
]
