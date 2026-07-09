"""
Main URL configuration for the Django project.

Backend responsibility:
- Expose project-level routes.
- Register the Django Admin interface.
- Include Django's built-in authentication routes.
- Delegate application-specific routes to miapp.urls.
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # Internal backoffice provided by Django Admin.
    path("admin/", admin.site.urls),

    # Built-in authentication routes provided by Django:
    # /login/
    # /logout/
    # /password_change/
    # /password_reset/
    path("", include("django.contrib.auth.urls")),

    # Application routes for the order management system.
    path("", include("miapp.urls")),
]