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
        "customer_name",
        "customer_email",
        "product_name",
        "quantity",
        "total_amount",
        "status",
        "created_at",
    )
    
    # Fields available in the Django Admin search bar
    search_fields = (
        "customer_name",
        "customer_email",
        "product_name",
    )
    
    # Sidebar filters available in the Django Admin list view
    list_filter = (
        "status",
        "created_at",
    )