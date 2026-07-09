# Order Management System 📦

Mini sistema web desarrollado con Django para gestionar pedidos de clientes mediante un flujo CRUD completo, autenticación, formularios, vistas protegidas, consultas avanzadas y una arquitectura basada en Class-Based Views.

## Objetivo

El objetivo de esta práctica es entrenar una arquitectura backend web con Django, entendiendo el flujo completo de una petición:

```text
URL
→ View
→ Form / ORM
→ Database
→ Context
→ Template
→ HTTP Response
```

El proyecto no se limita a mostrar datos. Implementa creación, lectura, actualización, eliminación, autenticación, control de acceso, listado avanzado de pedidos y documentación técnica del sistema.

## Estado actual

El proyecto se encuentra en una fase completa de desarrollo backend web.

Incluye:

- Modelo principal `Order` ampliado.
- Referencia interna automática para pedidos.
- Migraciones de base de datos.
- Django Admin configurado.
- Formularios con `ModelForm`.
- Formulario personalizado de registro basado en `UserCreationForm`.
- Listado público de pedidos.
- Detalle público de pedidos.
- Creación de pedidos protegida con autenticación.
- Actualización de pedidos protegida con autenticación.
- Eliminación de pedidos protegida con confirmación por POST.
- Login y logout usando el sistema de autenticación de Django.
- Navegación dinámica según `user.is_authenticated`.
- Búsqueda, filtro, ordenación y paginación en `/orders/`.
- Class-Based Views para los casos de uso web principales.
- Templates con herencia mediante `base.html`.

## Tecnologías utilizadas

- Python 3.14+
- Django 6.x
- SQLite3
- Django ORM
- Django Forms
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
| `forms.py` | Entrada y validación mediante formularios |
| `views.py` | Casos de uso HTTP mediante Class-Based Views |
| `templates/` | Presentación HTML |
| `admin.py` | Backoffice interno |
| `migrations/` | Evolución del esquema de base de datos |
| `README.md` | Documentación técnica del proyecto |

## Evolución a Class-Based Views

El proyecto comenzó con vistas basadas en funciones para entender de forma explícita el ciclo de una petición web: `request`, `GET`, `POST`, `form.is_valid()`, `form.save()`, `render()` y `redirect()`.

Después se evolucionó a Class-Based Views para reutilizar los patrones estándar de Django y reducir repetición en los casos de uso CRUD.

| Caso de uso | Class-Based View | Responsabilidad |
| --- | --- | --- |
| Home | `TemplateView` | Renderizar la página principal |
| Signup | `FormView` | Mostrar y procesar el formulario de registro |
| Listado | `ListView` | Consultar, filtrar, ordenar y paginar pedidos |
| Detalle | `DetailView` | Mostrar un pedido concreto |
| Crear | `CreateView` | Crear pedidos mediante `OrderForm` |
| Actualizar | `UpdateView` | Editar pedidos existentes |
| Eliminar | `DeleteView` | Confirmar y eliminar pedidos |

### Decisión técnica

La evolución a Class-Based Views no cambia la funcionalidad principal del sistema. Cambia la forma de organizar los casos de uso web.

Django se encarga del flujo estándar de renderizado, validación, búsqueda de objetos, guardado y redirección. El proyecto mantiene solo la configuración y las personalizaciones necesarias.

## Autenticación y control de acceso

El proyecto usa el sistema de autenticación de Django.

Django proporciona:

- `UserCreationForm`
- `login()`
- `logout`
- sesiones
- `request.user`
- `user.is_authenticated`
- `LoginRequiredMixin`

El programador decide:

- qué URL usa el registro;
- qué template muestra login y signup;
- a dónde redirige después del registro, login o logout;
- qué vistas deben protegerse;
- qué navegación ve cada tipo de usuario.

### Vistas públicas

| Vista | URL | Descripción |
| --- | --- | --- |
| `HomeView` | `/` | Página de inicio pública |
| `SignUpView` | `/signup/` | Registro de usuario |
| `LoginView` | `/login/` | Inicio de sesión proporcionado por Django |
| `OrderListView` | `/orders/` | Listado de pedidos |
| `OrderDetailView` | `/orders/<id>/` | Detalle de pedido |

### Vistas protegidas

| Vista | URL | Descripción |
| --- | --- | --- |
| `OrderCreateView` | `/orders/create/` | Crear pedido |
| `OrderUpdateView` | `/orders/<id>/edit/` | Actualizar pedido |
| `OrderDeleteView` | `/orders/<id>/delete/` | Eliminar pedido |

Las operaciones de escritura están protegidas con `LoginRequiredMixin` porque modifican datos persistidos.

## Formularios

El proyecto utiliza formularios para validar la entrada del usuario antes de persistir datos.

### `OrderForm`

`OrderForm` es un `ModelForm` conectado al modelo `Order`.

Permite crear y actualizar pedidos, pero no expone `order_reference`, `created_at` ni `updated_at`, porque son campos gestionados por el sistema.

Campos editables desde formulario:

- `customer_name`
- `customer_email`
- `product_name`
- `quantity`
- `total_amount`
- `shipping_address`
- `payment_method`
- `status`

Validaciones implementadas:

- Nombre de cliente no vacío.
- Nombre de producto no vacío.
- Cantidad mayor que cero.
- Importe total mayor que cero.

### `SignUpForm`

El proyecto incluye un formulario personalizado de registro basado en `UserCreationForm`.

Este formulario añade `email` como campo obligatorio y mantiene la validación de contraseñas integrada con Django.

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

Acceso local:

```text
http://127.0.0.1:8000/
```

## Usuario de prueba / superusuario

Superusuario de desarrollo para acceder al panel de administración:

```text
URL: http://127.0.0.1:8000/admin/
Usuario: admin
Contraseña: admin-1993
```

Si la contraseña no coincide en la base de datos local, se puede resetear con:

```bash
python3 manage.py changepassword admin
```

También se puede crear un nuevo superusuario con:

```bash
python3 manage.py createsuperuser
```

## Comandos principales

```bash
python3 manage.py check
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py changepassword admin
python3 manage.py runserver
python3 manage.py shell
```

## Comprobaciones finales

Antes de entregar el proyecto, ejecutar:

```bash
python3 manage.py check
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

Rutas a comprobar manualmente:

```text
/
/signup/
/login/
/logout/
/orders/
/orders/?q=laptop
/orders/?status=pending
/orders/?order=created_at&dir=desc
/orders/?q=laptop&status=pending&order=created_at&dir=desc&page=2
/orders/create/
/orders/1/
/orders/1/edit/
/orders/1/delete/
/admin/
```

Comportamiento esperado:

- Se puede iniciar sesión sin errores.
- Se puede cerrar sesión sin errores.
- El listado y el detalle son públicos.
- Crear, editar y eliminar requieren usuario autenticado.
- Los formularios muestran errores de validación.
- El listado permite combinar búsqueda, filtro, ordenación y paginación.
- Los parámetros GET se preservan al navegar entre páginas.
- El panel de administración permite gestionar pedidos.
- El proyecto arranca correctamente sin errores de sistema.

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

## Cobertura de requisitos de la actividad

| Requisito | Estado |
| --- | --- |
| ModelForm para el modelo principal | Cumplido |
| Crear registros | Cumplido |
| Editar registros | Cumplido |
| Validaciones básicas | Cumplido |
| Login y logout | Cumplido |
| Crear, editar y eliminar solo para autenticados | Cumplido |
| Listado y detalle públicos | Cumplido |
| Búsqueda por texto con `?q=` | Cumplido |
| Filtro adicional por estado | Cumplido |
| Filtros mediante GET | Cumplido |
| Orden con `?order=` | Cumplido |
| Lista blanca de campos ordenables | Cumplido |
| Dirección `?dir=asc|desc` | Cumplido |
| Paginación | Cumplido |
| Preservar parámetros GET en paginación | Cumplido |
| Herencia desde `base.html` | Cumplido |
| Barra de navegación dinámica | Cumplido |
| README con ejecución y URLs de ejemplo | Cumplido |

## Validaciones implementadas

- [x] Proyecto Django creado.
- [x] App `miapp` registrada.
- [x] Modelo `Order` creado y ampliado.
- [x] Migraciones creadas y aplicadas.
- [x] SQLite configurado como base de datos local.
- [x] Django Admin configurado.
- [x] `OrderForm` creado.
- [x] `SignUpForm` personalizado.
- [x] Listado público de pedidos.
- [x] Detalle público de pedidos.
- [x] Creación de pedidos con formulario.
- [x] Actualización de pedidos existentes.
- [x] Eliminación de pedidos con confirmación.
- [x] Registro de usuarios.
- [x] Login y logout.
- [x] Navegación dinámica según autenticación.
- [x] Protección de vistas privadas con `LoginRequiredMixin`.
- [x] Búsqueda, filtro, ordenación y paginación.
- [x] Manejo de recursos inexistentes mediante las Class-Based Views de Django.
- [x] Documentación técnica actualizada.

## Conceptos trabajados

- Modelos Django y ORM.
- Migraciones de base de datos.
- Django Admin.
- Function-Based Views.
- Class-Based Views.
- URLs y enrutamiento.
- `ModelForm`.
- `UserCreationForm`.
- GET y POST.
- Patrón POST → Redirect → GET.
- Autenticación con Django.
- Control de acceso con `LoginRequiredMixin`.
- Templates y herencia.
- Context como puente entre view y template.
- Búsqueda con parámetros GET.
- Filtros con QuerySet.
- Ordenación segura con lista blanca.
- Paginación.
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

### Class-Based Views

El CRUD se ha refactorizado a Class-Based Views para reutilizar patrones estándar de Django y reducir repetición en la capa de views.

### Alcance controlado

No se han introducido relaciones como `Customer`, `Product` u `OrderItem` porque el objetivo de la práctica es cerrar un sistema de pedidos autocontenido con flujo backend web completo.

## Mejoras futuras

- Separar `Customer` como entidad propia.
- Separar `Product` como entidad propia.
- Añadir `OrderItem` para permitir pedidos con múltiples productos.
- Añadir `choices` para `status` y `payment_method`.
- Añadir tests unitarios y tests de views.
- Añadir permisos por rol.
- Añadir relación `User → Order`.
- Añadir soft delete para pedidos históricos.
- Migrar de SQLite a PostgreSQL.
- Crear una API REST con Django REST Framework.

## Entrega

Formato requerido:

```text
.zip
```

Nombre recomendado del archivo:

```text
M5T2_Alvaro_Carrasco_Morera.zip
```

Antes de comprimir, excluir carpetas y archivos innecesarios como:

```text
venv/
__pycache__/
*.pyc
.DS_Store
```

## Repositorio

GitHub repository:

```text
https://github.com/acarras93-alt/django-order-management
```

## Estado

Current version:

```text
Django order management system with authentication, protected CRUD actions, advanced order listing, automatic order references, Class-Based Views and updated technical documentation.
```

```markdown

## Comprobaciones funcionales realizadas

Antes de la entrega se han verificado los siguientes flujos:

- Login y logout funcionan correctamente.
- El listado y el detalle de pedidos son públicos.
- Crear, editar y eliminar redirigen al login si el usuario no está autenticado.
- Crear, editar y eliminar funcionan correctamente con un usuario autenticado.
- La búsqueda, el filtro, la ordenación y la paginación funcionan sin romper la navegación.
- Los parámetros GET se preservan al navegar entre páginas.
- Django Admin permite acceder a `Orders` y abrir pedidos sin errores.
- El registro muestra el campo `email` y permite crear usuarios.
- El proyecto arranca correctamente y pasa `python3 manage.py check`.

El sistema cumple el flujo principal esperado: permite consultar pedidos de forma pública, protege las operaciones de escritura mediante autenticación,valida formularios, mantiene 
la navegación de búsqueda/filtros/ordenación y permite gestionar pedidos desde Django Admin.

### Rutas verificadas

```text

/
 /signup/
 /login/
 /logout/
 /orders/
 /orders/?q=laptop
 /orders/?status=pending
 /orders/?order=created_at&dir=desc
 /orders/?q=laptop&status=pending&order=created_at&dir=desc&page=2
 /orders/create/
 /orders/1/
 /orders/1/edit/
 /orders/1/delete/
 /admin/