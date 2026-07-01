"""
Define URL patterns for the orders app.
Each URL maps an HTTP request path to a view function.
"""
from django.urls import path
from . import views

app_name = "miapp"

urlpatterns = [
    # Public order list
    path("orders/", views.order_list, name="order_list"),
    
    # Order creation form
    path("orders/create/", views.order_create, name="order_create"),
    
    # Public order detail
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
]
