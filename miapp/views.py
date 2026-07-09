# Web request flow:
# URL routing -> View -> Form / ORM -> Context -> Template -> HTTP Response

# This file contains the web use cases of the application.
# Class-Based Views are used to reuse Django's standard CRUD patterns.
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy

# Implementando la arquitectura de Class-Based Views, Django se encarga internamente de renderizar usando las clases genéricas que importas.
from django.views.generic import (
    TemplateView,
    FormView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import OrderForm, SignUpForm
from .models import Order

# Capa views: representan los casos de uso HTTP de la aplicación.
# -> coordinan la petición HTTP con formularios, ORM, templates y redirecciones.
# Uso las Class-Based Views porque mi aplicación implementa casos de uso web estándar de CRUD.
# Django ya proporciona clases genéricas para estos patrones, lo que reduce repetición y hace el código más declarativo.

# Public read-only view: authentication is not required.
# modify persisted data.
class HomeView(TemplateView):
    """Public home page.
    
    Backend responsibility:
    - Render the main entry page.
    - Allow the template to show different links depending on authentication.
    """
    # TemplateView renderiza el template configurado para una página pública simple.
    template_name = "miapp/home.html"

# Implementamos el formulario de registro y la creación del usuario
# Public read-only view: authentication is not required.
# modify persisted data.
class SignUpView(FormView):
    """Register a new user
    
    Backend responsibility:
    - On GET: show an empty registration form
    - On POST: validate the submitted user data.
    - If valid: create the user, log them in and redirect to home.
    """
    # UserCreationForm es un formulario que Django proporciona para crear usuarios dentro de su sistema de autenticación.
    # FormView ya sabe mostrar formulario en GET y validar formulario en POST
    # Personalizo qué ocurre cuando el formulario es válido
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("miapp:home")
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)

# Representa el caso de uso de lectura avanzada de pedidos.
# Public read-only view: authentication is not required.
# modify persisted data.
class OrderListView(ListView):
    """
    Public view that shows all orders with search, filter, ordering
    and pagination.
    """

    model = Order
    template_name = "miapp/order_list.html"
    context_object_name = "orders"
    paginate_by = 10

    allowed_order_fields = {
        "customer_name": "customer_name",
        "product_name": "product_name",
        "total_amount": "total_amount",
        "created_at": "created_at",
        "updated_at": "updated_at",
        "status": "status",
    }
    # Decidir qué pedidos se consultan
    # Build the QuerySet used by the advanced order list.
    # This method centralizes search, filtering and safe ordering.
    def get_queryset(self):
        orders = Order.objects.all()

        query = self.request.GET.get("q", "").strip()

        if query:
            orders = orders.filter(
                Q(customer_name__icontains=query)
                | Q(customer_email__icontains=query)
                | Q(product_name__icontains=query)
                | Q(order_reference__icontains=query)
                | Q(payment_method__icontains=query)
            )

        status = self.request.GET.get("status", "").strip()

        if status:
            orders = orders.filter(status__iexact=status)

        order = self.request.GET.get("order", "created_at")
        direction = self.request.GET.get("dir", "desc")

        order_field = self.allowed_order_fields.get(order, "created_at")

        if direction == "desc":
            order_field = f"-{order_field}"

        return orders.order_by(order_field)

    # Añadir datos extra para el template
    # Add UI state to the template context.
    # This preserves search, filters and ordering across pagination links.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query_params = self.request.GET.copy()

        if "page" in query_params:
            query_params.pop("page")

        context["query"] = self.request.GET.get("q", "").strip()
        context["status"] = self.request.GET.get("status", "").strip()
        context["order"] = self.request.GET.get("order", "created_at")
        context["direction"] = self.request.GET.get("dir", "desc")
        context["query_params"] = query_params.urlencode()

        return context

# Consultar un pedido concreto
# Public read-only view: authentication is not required.
# modify persisted data.
class OrderDetailView(DetailView):
    """Public view that shows a single order."""
    # DetailView ya sabe buscar un objeto por primary key.
    
    model = Order
    template_name = "miapp/order_detail.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"

# Protected write view: authentication is required through LoginRequiredMixin.
# updates or deletes persisted Order data.
class OrderCreateView(LoginRequiredMixin, CreateView):
    """View that creates a new order."""
    # CreateView ya sabe:
    # - GET -> mostrar formulario
    # - POST -> validar formulario
    # - form_valid -> guardar objeto
    # - success_url -> redirigir después de guardar
    # - LoginRequiredMixin -> protege la view
    
    model = Order
    form_class = OrderForm
    template_name = "miapp/order_form.html"
    success_url = reverse_lazy("miapp:order_list")

# Consultar un pedido concreto par editarlo.
# Protected write view: authentication is required through LoginRequiredMixin.
# updates or deletes persisted Order data.
class OrderUpdateView(LoginRequiredMixin, UpdateView):
    """View that updates an existing order."""
    # UpdateView ya sabe:
    # - GET -> buscar el objeto y mostrar formulario con datos actuales.
    # - POST -> validar datos y actualizar esa instancia.
    # - get_success_url() -> permite redirigir al detalle del pedido editado.
    
    model = Order
    form_class = OrderForm
    template_name = "miapp/order_form.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"

    def get_success_url(self):
        return reverse_lazy(
            "miapp:order_detail",
            kwargs={"order_id": self.kwargs["order_id"]},
        )

# Protected write view: authentication is required through LoginRequiredMixin.
# Consultar un pedido concreto para eliminarlo.
class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """View that deletes an existing order."""
    # DeleteView ya sabe:
    # - GET -> mostrar confirmación
    # - POST -> borrar objeto
    # - succes_url -> redirigir después del borrado
    
    model = Order
    template_name = "miapp/order_confirm_delete.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"
    success_url = reverse_lazy("miapp:order_list")