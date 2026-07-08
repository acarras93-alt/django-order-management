# CICLO DE UNA PETICION WEB
# 1. Ejecución -> Se invoca a la vista (ej: views.order_update) asociada al patrón, desde la ruta que coincide
# 2. Proceso -> La vista consulta la base de datos para obtener los pedidos
# 3. Contexto -> La vista prepara los datos en un diccionario('contexto')
# 4. Template -> La vista renderiza el template HTML pasándole el contexto
# 5. Respuesta -> La vista devuelve un objeto 'HTTPResponse' al navegador del usuario
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
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

# Capa views: coordina el flujo completo.
# Representa los casos de uso HTTP de la aplicación.
# Este proyecto contien las Class-Based Views que conectan las rutas con la lógica web: listado, detalle, creación, actualización, eliminación y registro de usuarios.

# Pagina de inicio pública
class HomeView(TemplateView):
    """Public home page.
    
    Backend responsibility:
    - Render the main entry page.
    - Allow the template to show different links depending on authentication.
    """
    # TemplateView ya sabe renderizar un template.
    template_name = "miapp/home.html"

class SignUpView(FormView):
    """Register a new user
    
    Backend responsibility:
    - On GET: show an empty registration form
    - On POST: validate the submitted user data.
    - If valid: create the user, log them in and redirect to home.
    """
    # UserCreationForm es un formulario que Django proporciona para crear usuarios dentro de su sistema de autenticación
    # FormView ya sabe mostrar formulario en GET y validar formulario en POST
    # Personalizo qué ocurre cuando el formulario es válido
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("miapp:home")
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)

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
    # decidir qué pedidos se consultan
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

    # añadir datos extra para el template
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
class OrderDetailView(DetailView):
    """Public view that shows a single order."""
    # DetailView ya sabe buscar un objeto por primary key.
    
    model = Order
    template_name = "miapp/order_detail.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"

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