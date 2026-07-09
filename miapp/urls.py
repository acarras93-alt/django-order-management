"""
Define URL patterns for the orders app.
Each URL maps an HTTP request path to a Class-Based View.
"""
# La capa de enrutamiento define la conexión entre una ruta y una vista.
# Cuando llega una petición HTTP, Django necesita saber qué código debe ejecutar.
# CICLO DE UNA PETICIÓN
# 1. Peticion -> El navegador del usuario solicita una URL ej: /orders
# 2. Enrutamiento -> Django busca una coincidencia/patron que encaje dentro de este archivo: urls.py 
# 3. Ejecución -> Se invoca a la vista (ej: views.order_update) asociada al patrón
# 4. Respuesta -> La vista devuelve un objeto 'HTTPResponse' al navegador

# App-level URL routing.
# Each route maps an HTTP path to a Class-Based View.
# as_view() converts the class into a callable view for Django.
from django.urls import path
from .views import (
    HomeView,
    SignUpView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
)

app_name = "miapp"

# Class-Based Views are converted into callable views through as_view().
# The name argument provides a stable route alias for templates and redirects.
urlpatterns = [
    # Public routes
    path("", HomeView.as_view(), name="home"), # Home page
    path("signup/", SignUpView.as_view(), name="signup"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:order_id>/", OrderDetailView.as_view(), name="order_detail"),

    # Protected write routes
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:order_id>/edit/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:order_id>/delete/", OrderDeleteView.as_view(), name="order_delete"),
]
