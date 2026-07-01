from django.shortcuts import render, get_object_or_404

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