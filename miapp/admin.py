"""
Register the Order model in the admin panel
and connect it with its Django Admin configuration.
"""

from django.contrib import admin # Imports Django Admin tools to register and configure models
from .models import Order # Imports the Order model from the current app

# Admin configuration for the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Columns displayed in the Django Admin list view 
    list_display = (
        "order_reference",
        "customer_name",
        "product_name",
        "quantity",
        "total_amount",
        "status",
        "payment_method",
        "created_at",
        "updated_at",
    )
    # Sidebar filters available in the Django Admin list view
    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )
    
    # Fields available in the Django Admin search bar
    search_fields = (
        "order_reference",
        "customer_name",
        "customer_email",
        "product_name",
    )
    
    readonly_fields = (
        "order_reference",
        "created_at",
        "updated_at",
    )