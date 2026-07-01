from django.shortcuts import render, redirect, get_object_or_404

from .forms import OrderForm
from .models import Order  # Imports the Order model from the current app


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