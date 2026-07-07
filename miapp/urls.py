"""
Define URL patterns for the orders app.
Each URL maps an HTTP request path to a view function.
"""
# Este fichero define la conexión entre una ruta y una vista
# CICLO DE UNA PETICIÓN
# 1. Peticion -> El navegador del usuario solicita una URL ej: /orders
# 2. Enrutamiento -> Django busca una coincidencia/patron que encaje dentro de este archivo: urls.py 
# 3. Ejecución -> Se invoca a la vista (ej: views.order_update) asociada al patrón
# 4. Respuesta -> La vista devuelve un objeto 'HTTPResponse' al navegador

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

# Django cuando alguien entre en la ruta ej:orders/ quiero que llames a la funcion ej: views.order_list que tengo en mi archivo de vistas
# name es solo un apodo que le ponemos a la ruta para referirnos a ella en otras partes del codigo
urlpatterns = [
    
    path("", HomeView.as_view(), name="home"), # Home page
    path("signup/", SignUpView.as_view(), name="signup"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:order_id>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:order_id>/edit/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:order_id>/delete/", OrderDeleteView.as_view(), name="order_delete"),
]
