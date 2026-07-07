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
from . import views

app_name = "miapp"

# Django cuando alguien entre en la ruta ej:orders/ quiero que llames a la funcion ej: views.order_list que tengo en mi archivo de vistas
# name es solo un apodo que le ponemos a la ruta para referirnos a ella en otras partes del codigo
urlpatterns = [
    
    path("", views.home, name="home"), # Home page
    path("signup/", views.signup, name="signup"), # User registration

    
    path("orders/", views.order_list, name="order_list"), # Public order list
    path("orders/create/", views.order_create, name="order_create"), # Order creation form
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"), # Public order detail
    path("orders/<int:order_id>/edit/", views.order_update, name="order_update"),
    path("orders/<int:order_id>/delete/", views.order_delete, name="order_delete"),
]
