# CICLO DE UNA PETICION WEB
# 1. Ejecución -> Se invoca a la vista (ej: views.order_update) asociada al patrón, desde la ruta que coincide
# 2. Proceso -> La vista consulta la base de datos para obtener los post
# 3. Contexto -> La vista prepara los datos en un diccionario('contexto')
# 4. Template -> La vista renderiza el template HTML pasándole el contexto
# 5. Respuesta -> La vista devuelve un objeto 'HTTPResponse' al navegador del usuario
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import OrderForm
from .models import Order  

# Pagina de inicio pública
def home(request):
    """Public home page.
    
    Backend responsibility:
    - Receive the HTTP request.
    - Render the main entry page.
    - allow the template to show different links depending on authentication.
    """
    
    return render(request, "miapp/home.html")

def signup(request):
    """Register a new user
    
    Backend responsibility:
    - On GET: show an empty registration form
    - On POST: validate the submitted user data.
    - If valid: create the user, log them in and redirect to home.
    """
    # Si el usuario envía el formulário, procesamos los datos
    if request.method == "POST":
        # UserCreationForm receives username and password data from the browser.
        form = UserCreationForm(request.POST)

        # Django validates username and password rules before creating the user.
        if form.is_valid():
            user = form.save()

            # After registration, the user is automatically logged in.
            login(request, user)

            return redirect("miapp:home")

    else:
        # Empty form for the first page load.
        form = UserCreationForm()

    context = {
        "form": form,
    }
    # Renderizamos el template pasando el formulario al contexto.
    return render(request, "registration/signup.html", context)

def order_list(request):
    """
    Public view that shows all orders.

    Backend mental model:
    - Equivalent to list_orders() in a service layer.
    - Uses the Django ORM instead of a JSON repository.
    - Sends the result to the template through context.
    """
    # ORM query: gets all Order records from the database
    orders = Order.objects.all()

    # Context: data sent from the backend view to the HTML template
    context = {
        "orders": orders,
    }
    
    # Render: returns an HTTP response with the generated HTML
    return render(request, "miapp/order_list.html", context)


def order_detail(request, order_id):
    """
    Public view that shows a single order.

    Backend mental model:
    - Equivalent to find_order_by_id(order_id).
    - If the order does not exist, Django returns a 404 response.
    """
    # ORM query with automatic 404 if the object does not exist
    order = get_object_or_404(Order, id=order_id)
    
    # Context: data sent from the backend view to the HTML template
    context = {
        "order": order,
    }

    # Renders the order detail template with the selected order
    return render(request,"miapp/order_detail.html",context)

@login_required
def order_create(request):
    """
    View that creates a new order.

    Backend responsibility:
    - On GET: show an empty form.
    - On POST: validate incoming data.
    - If valid: save the new order.
    - Redirect to the order list after saving.
    """

    if request.method == "POST":
        # The form receives data submitted by the browser.
        form = OrderForm(request.POST)

        # Django validates the form before saving anything.
        if form.is_valid():
            form.save()
            return redirect("miapp:order_list")

    else:
        # Empty form for the first page load.
        form = OrderForm()

    context = {
        "form": form,
    }

    return render(request, "miapp/order_form.html", context)

@login_required
def order_update(request, order_id):
    """
    View that updates an existing order.

    Backend responsibility:
    - Only authenticated users can edit orders.
    - Load the existing Order by ID.
    - On GET: show the form with the current order data.
    - On POST: validate submitted changes.
    - If valid: update the order and redirect to detail.
    """

    # Get the order or return 404 if it does not exist.
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        # The form receives submitted data and updates the existing instance.
        form = OrderForm(request.POST, instance=order)

        # Django validates the form before saving changes.
        if form.is_valid():
            form.save()
            return redirect("miapp:order_detail", order_id=order.pk)

    else:
        # The form is pre-filled with the current order data.
        form = OrderForm(instance=order)

    context = {
        "form": form,
        "order": order,
    }

    return render(request, "miapp/order_form.html", context)


@login_required
def order_delete(request, order_id):
    """
    View that deletes an existing order.

    Backend responsibility:
    - Only authenticated users can delete orders.
    - Load the existing Order by ID.
    - On GET: show a confirmation page.
    - On POST: delete the order and redirect to list.
    """

    # Get the order or return 404 if it does not exist.
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        # Delete the existing order from the database.
        order.delete()
        return redirect("miapp:order_list")

    context = {
        "order": order,
    }

    return render(request, "miapp/order_confirm_delete.html", context)