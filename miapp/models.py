"""
Define the Order model as the main domain entity used to store customer order data in the database.

Order:
- customer_name
- customer_email
- product_name
- quantity
- total_amount
- shipping_address
- payment_method
- order_reference
- status
- created_at
- updated_at

System-managed fields:
order_reference -> generated automatically before the first save.
created_at -> set automatically when the order is created.
updated_at -> updated automatically whenever the order is saved.
"""
# Model responsibility:
# Defines the complete persistent structure and system-managed behavior of an Order.
from uuid import uuid4
from django.db import models

class Order(models.Model):
    """
    Main domain model used to store customer orders in the database.

    Backend responsibility:
    - Represent a customer order.
    - Store customer, product, payment, shipping and status information.
    - Generate an internal unique order reference automatically.
    """

    # Customer information
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()

    # Product information
    product_name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField()

    # Financial information
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Shipping information
    shipping_address = models.CharField(max_length=255, blank=True)

    # Payment information
    payment_method = models.CharField(max_length=50, blank=True)

    # Internal order tracking
    order_reference = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    # Order status and timestamps
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_order_reference(self):
        """
        Generate a unique internal order reference.

        Example:
        ORD-A1B2C3D4
        """

        while True:
            reference = f"ORD-{uuid4().hex[:8].upper()}"

            if not Order.objects.filter(order_reference=reference).exists():
                return reference

    def save(self, *args, **kwargs):
        """
        Save the order.

        Backend responsibility:
        - If the order does not have an internal reference yet,
        generate one before saving.
        - Then delegate the actual database persistence to Django.
        """

        if not self.order_reference:
            self.order_reference = self.generate_order_reference()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_reference} - {self.customer_name} - {self.product_name}"