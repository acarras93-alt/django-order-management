"""
Define URL patterns for the orders app.
Each URL maps an HTTP request path to a view function.
"""
from django.urls import path
from . import views

app_name = "miapp"

urlpatterns = [
    
    path("", views.home, name="home"), # Home page
    path("signup/", views.signup, name="signup"), # User registration

    
    path("orders/", views.order_list, name="order_list"), # Public order list
    path("orders/create/", views.order_create, name="order_create"), # Order creation form
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"), # Public order detail
    path("orders/<int:order_id>/edit/", views.order_update, name="order_update"),
    path("orders/<int:order_id>/delete/", views.order_delete, name="order_delete"),
]
