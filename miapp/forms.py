# CICLO DE UNA PETICION WEB
# 1. View -> La view recibe la request y decide que hacer
# Aquí entra la lógica
# GET -> mostrar formulario vacío
# POST -> procesar formulario enviado
# 2. Form -> El formulario entra aquí
# Responsabilidad:
# - recibir datos del usuario
# - validar esos datos
# - preparar datos limpios
# - permitir guardar si es ModelForm
# 3. ORM -> Database
# Si el formulario es valido, la view guarda usando el ORM
# Ejemplo form.save()
# 4. View -> La view prepara los datos para el template(context)
# 5. Template -> Django renderiza el HTML
# 6. HTTP Response -> Django devuelve el HTML al navegador

# forms.ModelForm -> Crear o actualizar Order
# forms.Form -> Contacto, búsqueda o filtros
# Signup con UserCreationForm -> caso especial: Django ya te da un formulario de autenticación/usuarios
"""
Forms for the orders application.

This file contains the input and validation layer for Order objects.
The form receives data from the browser, validates it and prepares it
to be saved through the Django ORM.

"""

from django import forms
from .models import Order

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# 1.Formulario del dominio Order
# - Definimos qué datos del pedido puede rellenar el formulario.
# - El formulario contiene solo los campos que el usuario puede introducir o modificar.
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
# El parametro widgets permite personalizar el tipo del campo visual.
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

# 2. Formulario personalizado de registro.
class SignUpForm(UserCreationForm):
    """
    Custom signup form for user registration.

    Backend responsibility:
    - Extend Django's UserCreationForm.
    - Add email as a required registration field.
    - Keep password validation integrated with Django Auth.
    """
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "email@example.com",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

# 3. Formulario de búsqueda/filtros.
class OrderSearchForm(forms.Form):

    """
    Form used to validate search and filter parameters for the order list.

    Backend responsibility:
    - Validate GET parameters used in the advanced order list.
    - Avoid treating raw URL parameters as trusted input.
    - Keep search and filtering input separate from Order creation/update.
    """
    # Controlar una consulta GET
    query = forms.CharField(required=False)
    status = forms.CharField(required=False)
    order = forms.CharField(required=False)
    direction = forms.CharField(required=False)

    def clean_order(self):
        """
        Validate the ordering field.

        Backend rule:
        The user can only order by allowed fields.
        """

        order = self.cleaned_data["order"]
        allowed_order_fields = [
            "customer_name",
            "product_name",
            "total_amount",
            "created_at",
            "updated_at",
            "status",
        ]

        if order and order not in allowed_order_fields:
            return "created_at"

        return order or "created_at"

    def clean_direction(self):
        """
        Validate ordering direction.

        Backend rule:
        Direction can only be asc or desc.
        """

        direction = self.cleaned_data["direction"]

        if direction not in ["asc", "desc"]:
            return "desc"

        return direction