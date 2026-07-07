"""
Forms for the orders application.

This file contains the input and validation layer for Order objects.
The form receives data from the browser, validates it and prepares it
to be saved through the Django ORM.
"""

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Form connected to the Order model.

    Backend responsibility:
    - Expose only the fields that the user is allowed to fill.
    - Validate incoming data before saving it to the database.
    - Create or update Order records through the ORM.
    """

    class Meta:
        model = Order

        # These are the fields that the user can fill from the web form.
        # order_reference, created_at and updated_at are excluded because
        # they are managed automatically by the system.
        fields = [
            "customer_name",
            "customer_email",
            "product_name",
            "quantity",
            "total_amount",
            "shipping_address",
            "payment_method",
            "status",
        ]

        widgets = {
            "customer_name": forms.TextInput(
                attrs={
                    "placeholder": "Customer name",
                }
            ),
            "customer_email": forms.EmailInput(
                attrs={
                    "placeholder": "customer@example.com",
                }
            ),
            "product_name": forms.TextInput(
                attrs={
                    "placeholder": "Product name",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "min": 1,
                }
            ),
            "total_amount": forms.NumberInput(
                attrs={
                    "min": 0.01,
                    "step": 0.01,
                }
            ),
            "shipping_address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Shipping address",
                }
            ),
            "payment_method": forms.TextInput(
                attrs={
                    "placeholder": "card, paypal, bank transfer...",
                }
            ),
            "status": forms.TextInput(
                attrs={
                    "placeholder": "pending, confirmed, shipped...",
                }
            ),
        }

    def clean_customer_name(self):
        """
        Validate customer name.

        Backend rule:
        A customer name cannot be empty or only spaces.
        """

        customer_name = self.cleaned_data["customer_name"]

        if not customer_name.strip():
            raise forms.ValidationError("Customer name cannot be empty.")

        return customer_name

    def clean_product_name(self):
        """
        Validate product name.

        Backend rule:
        A product name cannot be empty or only spaces.
        """

        product_name = self.cleaned_data["product_name"]

        if not product_name.strip():
            raise forms.ValidationError("Product name cannot be empty.")

        return product_name

    def clean_quantity(self):
        """
        Validate quantity.

        Backend rule:
        The quantity must be greater than zero.
        """

        quantity = self.cleaned_data["quantity"]

        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")

        return quantity

    def clean_total_amount(self):
        """
        Validate total amount.

        Backend rule:
        The total amount must be greater than zero.
        """

        total_amount = self.cleaned_data["total_amount"]

        if total_amount <= 0:
            raise forms.ValidationError("Total amount must be greater than zero.")

        return total_amount