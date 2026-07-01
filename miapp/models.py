"""
Define the Order model as the main domain entity
used to store customer order data in the database.
"""

from django.db import models # Imports Django ORM tools to define database models and fields


# Main domain model used to store customer orders in the database
class Order(models.Model):
    # Customer information
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    
    # Order information
    product_name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Order status and creation date
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    # Human-readable representation for Django admin and shell
    def __str__(self):
        return f"{self.customer_name} - {self.product_name}"