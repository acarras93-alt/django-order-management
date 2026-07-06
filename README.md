# Order Management System 📦

Mini sistema web desarrollado con Django para gestionar pedidos de clientes mediante un flujo CRUD completo, autenticación, formularios, vistas protegidas y consultas avanzadas.

## Objetivo

El objetivo de esta práctica es entrenar una arquitectura backend web con Django, entendiendo el flujo completo:

```text
URL
→ View
→ Form / ORM
→ Database
→ Context
→ Template
→ HTTP Response
```

El proyecto no se limita a mostrar datos. Implementa creación, lectura, actualización, eliminación, autenticación, control de acceso y listado avanzado de pedidos.

## Estado actual

El proyecto se encuentra en una fase completa de desarrollo backend web.

Incluye:

- Modelo principal `Order` ampliado.
- Referencia interna automática para pedidos.
- Migraciones de base de datos.
- Django Admin configurado.
- Listado público de pedidos.
- Detalle público de pedidos.
- Creación de pedidos protegida con autenticación.
- Actualización de pedidos protegida con autenticación.
- Eliminación de pedidos protegida con confirmación por POST.
- Registro de usuarios.
- Login y logout usando el sistema de autenticación de Django.
- Navegación dinámica según `user.is_authenticated`.
- Búsqueda, filtro, ordenación y paginación en `/orders/`.
- Manejo de errores mediante `get_object_or_404()`.
- Templates con herencia mediante `base.html`.

## Tecnologías utilizadas

- Python 3.14+
- Django 6.x
- SQLite3
- Django ORM
- Django Templates
- Django Authentication
- HTML

## Modelo principal: `Order`

`Order` representa la entidad principal del dominio de pedidos.

A nivel funcional, actúa como la cabecera básica de un pedido dentro de una tienda. Almacena información del cliente, producto, importe, envío, pago, referencia interna, estado y trazabilidad temporal.

A nivel técnico, hereda de `models.Model`, por lo que Django lo gestiona mediante el ORM y lo traduce a una tabla de base de datos mediante migraciones.

### Campos del modelo

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `customer_name` | `CharField(120)` | Nombre del cliente |
| `customer_email` | `EmailField` | Email del cliente |
| `product_name` | `CharField(150)` | Nombre del producto |
| `quantity` | `PositiveIntegerField` | Cantidad pedida |
| `total_amount` | `DecimalField(10,2)` | Importe total del pedido |
| `shipping_address` | `CharField(255, blank=True)` | Dirección de envío |
| `payment_method` | `CharField(50, blank=True)` | Método de pago |
| `order_reference` | `CharField(50, unique=True, blank=True, null=True, editable=False)` | Referencia interna generada por el sistema |
| `status` | `CharField(30)` | Estado del pedido |
| `created_at` | `DateTimeField(auto_now_add=True)` | Fecha de creación |
| `updated_at` | `DateTimeField(auto_now=True)` | Fecha de última actualización |

### Referencia interna del pedido

El campo `order_reference` separa el identificador técnico de base de datos (`id`) de una referencia funcional más adecuada para administración, búsqueda o comunicación.

Ejemplo:

```text
ORD-A1B2C3D4
```

La referencia se genera automáticamente antes de guardar el pedido si todavía no existe.

## Capas principales del proyecto

| Archivo o carpeta | Responsabilidad |
| --- | --- |
| `settings.py` | Configuración global del proyecto |
| `proyecto_web_inicial/urls.py` | Enrutamiento principal |
| `miapp/urls.py` | Contrato HTTP de la aplicación |
| `models.py` | Entidad `Order` y persistencia ORM |
| `forms.py` | Validación de entrada mediante `ModelForm` |
| `views.py` | Casos de uso HTTP |
| `templates/` | Presentación HTML |
| `admin.py` | Backoffice interno |
| `migrations/` | Evolución del esquema de base de datos |
| `README.md` | Documentación técnica del proyecto |

## Flujo backend principal

```text
Request HTTP
→ URL routing
→ View
→ Form / ORM
→ Database
→ Context
→ Template
→ Response HTTP
```

## Autenticación y control de acceso

El proyecto usa el sistema de autenticación de Django.

Django proporciona:

- `UserCreationForm`
- `login()`
- `logout`
- sesiones
- `request.user`
- `user.is_authenticated`
- `login_required`

El programador decide:

- qué URL usa el registro;
- qué template muestra login y signup;
- a dónde redirige después del registro, login o logout;
- qué vistas deben protegerse;
- qué navegación ve cada tipo de usuario.

## Vistas públicas

| Vista | URL | Descripción |
| --- | --- | --- |
| `home` | `/` | Página de inicio pública |
| `signup` | `/signup/` | Registro de usuario |
| `login` | `/login/` | Inicio de sesión |
| `order_list` | `/orders/` | Listado de pedidos |
| `order_detail` | `/orders/<id>/` | Detalle de pedido |

## Vistas protegidas

| Vista | URL | Descripción |
| --- | --- | --- |
| `order_create` | `/orders/create/` | Crear pedido |
| `order_update` | `/orders/<id>/edit/` | Actualizar pedido |
| `order_delete` | `/orders/<id>/delete/` | Eliminar pedido |

Las operaciones de escritura están protegidas con `login_required` porque modifican datos persistidos.

## URLs principales

| URL | Método | Descripción |
| --- | --- | --- |
| `/` | GET | Página de inicio |
| `/admin/` | GET | Panel de administración |
| `/signup/` | GET / POST | Registro de usuario |
| `/login/` | GET / POST | Inicio de sesión |
| `/logout/` | POST | Cierre de sesión |
| `/orders/` | GET | Listado avanzado de pedidos |
| `/orders/create/` | GET / POST | Crear pedido |
| `/orders/<id>/` | GET | Detalle de pedido |
| `/orders/<id>/edit/` | GET / POST | Actualizar pedido |
| `/orders/<id>/delete/` | GET / POST | Confirmar y eliminar pedido |

## Listado avanzado

La ruta `/orders/` permite búsqueda, filtro, ordenación y paginación mediante parámetros GET.

Ejemplos:

```text
/orders/?q=laptop
/orders/?status=pending
/orders/?order=created_at&dir=desc
/orders/?q=laptop&status=pending&order=created_at&dir=desc&page=2
```

### Parámetros disponibles

| Parámetro | Descripción |
| --- | --- |
| `q` | Búsqueda por texto |
| `status` | Filtro por estado |
| `order` | Campo de ordenación |
| `dir` | Dirección: `asc` o `desc` |
| `page` | Página actual |

La ordenación se controla mediante una lista blanca de campos permitidos para evitar ordenar directamente por valores recibidos desde la URL.

## Formularios

El proyecto utiliza `OrderForm` como capa de entrada y validación.

`OrderForm` permite crear y actualizar pedidos, pero no expone `order_reference`, porque esa referencia es generada por el sistema.

Campos editables desde formulario:

- `customer_name`
- `customer_email`
- `product_name`
- `quantity`
- `total_amount`
- `shipping_address`
- `payment_method`
- `status`

## Templates principales

| Template | Responsabilidad |
| --- | --- |
| `templates/miapp/base.html` | Plantilla base y navegación común |
| `templates/miapp/home.html` | Página de inicio |
| `templates/miapp/order_list.html` | Listado avanzado de pedidos |
| `templates/miapp/order_detail.html` | Detalle de pedido |
| `templates/miapp/order_form.html` | Formulario de creación y edición |
| `templates/miapp/order_confirm_delete.html` | Confirmación de borrado |
| `templates/registration/login.html` | Formulario de login |
| `templates/registration/signup.html` | Formulario de registro |

## Instalación y configuración

### 1. Activar entorno virtual

```bash
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
python3 -m pip install -r requirements.txt
```

### 3. Crear migraciones

```bash
python3 manage.py makemigrations
```

### 4. Aplicar migraciones

```bash
python3 manage.py migrate
```

### 5. Crear superusuario

```bash
python3 manage.py createsuperuser
```

### 6. Ejecutar servidor

```bash
python3 manage.py runserver
```

## Comandos principales

```bash
python3 manage.py check
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
python3 manage.py shell
```

## Estructura del proyecto

```text
proyecto_web/
├── manage.py
├── README.md
├── requirements.txt
├── db.sqlite3
├── proyecto_web_inicial/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── miapp/
    ├── admin.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    │   ├── 0001_initial.py
    │   ├── 0002_*.py
    │   └── __init__.py
    └── templates/
        ├── miapp/
        │   ├── base.html
        │   ├── home.html
        │   ├── order_list.html
        │   ├── order_detail.html
        │   ├── order_form.html
        │   └── order_confirm_delete.html
        └── registration/
            ├── login.html
            └── signup.html
```

## Validaciones implementadas

- [x] Proyecto Django creado.
- [x] App `miapp` registrada.
- [x] Modelo `Order` creado y ampliado.
- [x] Migraciones creadas y aplicadas.
- [x] SQLite configurado como base de datos local.
- [x] Django Admin configurado.
- [x] `OrderForm` creado.
- [x] Listado público de pedidos.
- [x] Detalle público de pedidos.
- [x] Creación de pedidos con formulario.
- [x] Actualización de pedidos existentes.
- [x] Eliminación de pedidos con confirmación.
- [x] Registro de usuarios.
- [x] Login y logout.
- [x] Navegación dinámica según autenticación.
- [x] Protección de vistas privadas con `login_required`.
- [x] Búsqueda, filtro, ordenación y paginación.
- [x] Manejo de 404 con `get_object_or_404()`.
- [x] Documentación técnica actualizada.

## Conceptos trabajados

- Modelos Django y ORM.
- Migraciones de base de datos.
- Django Admin.
- Function-based views.
- URLs y enrutamiento.
- `ModelForm`.
- GET y POST.
- Patrón POST → Redirect → GET.
- Autenticación con Django.
- Control de acceso con `login_required`.
- Templates y herencia.
- Context como puente entre view y template.
- Búsqueda con parámetros GET.
- Filtros con QuerySet.
- Ordenación segura con lista blanca.
- Paginación.
- Manejo de errores HTTP 404.
- Separación de responsabilidades por capas.

## Decisiones técnicas relevantes

### Referencia interna automática

`order_reference` se genera automáticamente en el modelo para evitar que el usuario tenga que introducir una referencia manual.

### Escritura protegida

Las operaciones de creación, edición y borrado requieren autenticación.

### Borrado mediante POST

El borrado no se ejecuta directamente por GET. Primero se muestra una confirmación y después se elimina mediante POST.

### Ordenación segura

La ordenación del listado avanzado usa una lista blanca de campos permitidos. No se ordena directamente por cualquier valor recibido desde la URL.

## Mejoras futuras

- Separar `Customer` como entidad propia.
- Separar `Product` como entidad propia.
- Añadir `OrderItem` para permitir pedidos con múltiples productos.
- Añadir `choices` para `status` y `payment_method`.
- Añadir tests unitarios y tests de views.
- Añadir permisos por rol.
- Añadir soft delete para pedidos históricos.
- Migrar de SQLite a PostgreSQL.
- Crear una API REST con Django REST Framework.

## Repositorio

GitHub repository:

```text
https://github.com/acarras93-alt/django-order-management
```

## Estado

Current version:

```text
Django order management system with authentication, protected CRUD actions,
advanced order listing, automatic order references and updated technical documentation.
```
