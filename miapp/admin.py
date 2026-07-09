"""
Register the Order model in the admin panel and connect it 
with its Django Admin configuration.
"""
# Admin responsibility:
# Configure the internal backoffice used to list, search, filter and review orders.
from django.contrib import admin # Imports Django Admin tools to register and configure models
from .models import Order # Imports the Order model from the current app

# Admin configuration for the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for the Order Model.
    
    Backend responsibility:
    - Provide an internal backoffice for managing orders.
    - Display relevant orde information.
    - Enable search, filtering and ordering.
    - Protect system-generated fields from manual editing.
    """
    # Columns displayed in the Django Admin list view.
    # Define que columnas se ven el listado del admin.
    list_display = (
        "order_reference",
        "customer_name",
        "customer_email",
        "product_name",
        "quantity",
        "total_amount",
        "status",
        "payment_method",
        "created_at",
        "updated_at",
    )
    
    # Clickable columns in the list view.
    # Define que columnas son clicables para entrar al detalle.
    list_display_links = (
        "order_reference",
        "customer_name",
    )
    
    # Sidebar filters available in the Django Admin list view
    # Permite filtrar pedidos por estado, método de pago y fechas.
    list_filter = (
        "status",
        "payment_method",
        "created_at",
        "updated_at",
    )
    
    # Fields available in the Django Admin search bar
    # Permite buscar por referencia, cliente, email o producto
    search_fields = (
        "order_reference",
        "customer_name",
        "customer_email",
        "product_name",
    )
    
    # Default ordering in the admin list view.
    # Muestra los pedidos más recientes
    ordering = (
        "-created_at",
    )
    
    # Date navigation by creation date.
    # Añade navegación temporal por fecha de creación
    date_hierarchy = "created_at"

    # Number of rows displayed per page.
    # Limita cuantos pedidos aparecen por página.
    list_per_page = 20
    
    # Fields that should not be manually edited.
    # Protege campos generados por el sistema
    readonly_fields = (
        "display_order_reference",
        "created_at",
        "updated_at",
    )
    
    # Organize the detail form into logical sections.
    # Organiza el formulario interno del admin por bloques funcionales
    fieldsets = (
        (
            "Customer information",
            {
                "fields": (
                    "customer_name",
                    "customer_email",
                )
            },
        ),
        (
            "Product information",
            {
                "fields": (
                    "product_name",
                    "quantity",
                    "total_amount",
                )
            },
        ),
        (
            "Shipping and payment",
            {
                "fields": (
                    "shipping_address",
                    "payment_method",
                )
            },
        ),
        (
            "Order tracking",
            {
                "fields": (
                    "display_order_reference",
                    "status",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def display_order_reference(self, obj):
        """Display the internal order reference as a read-only admin field."""
        if obj.order_reference:
            
            return obj.order_reference

        return "-"
    
    display_order_reference.short_description = "Order reference"