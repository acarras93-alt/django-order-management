# Order Management System 📦

Mini CRUD básico desarrollado con Django para gestionar pedidos de clientes.

## Objetivo

El objetivo de esta práctica es trabajar con modelos, administración, vistas, URLs y templates en Django, mostrando datos dinámicos desde la base de datos.

## ✨ Funcionalidades

- **Modelo principal:** `Order` con 8 campos
- **Gestión de pedidos** desde Django Admin con búsqueda y filtros
- **Listado público** de todos los pedidos
- **Detalle público** de cada pedido individual
- **Manejo de errores:** Respuesta 404 para IDs inexistentes
- **Templates** con herencia mediante `base.html`
- **Base de datos:** SQLite3 con 4 pedidos de ejemplo

## 📋 Modelo Principal: Order

Campos del modelo `Order`:

| Campo            | Tipo                 | Descripción              |
| ---------------- | -------------------- | ------------------------ |
| `customer_name`  | CharField(120)       | Nombre del cliente       |
| `customer_email` | EmailField           | Email del cliente        |
| `product_name`   | CharField(150)       | Nombre del producto      |
| `quantity`       | PositiveIntegerField | Cantidad pedida          |
| `total_amount`   | DecimalField(10,2)   | Monto total              |
| `status`         | CharField(30)        | Estado del pedido        |
| `created_at`     | DateTimeField        | Fecha de creación (auto) |

## 🌐 URLs Principales

| URL             | Método | Descripción                     |
| --------------- | ------ | ------------------------------- |
| `/admin/`       | GET    | Panel de administración Django  |
| `/orders/`      | GET    | Listado de todos los pedidos    |
| `/orders/<id>/` | GET    | Detalle de un pedido específico |
| `/orders/999/`  | GET    | Retorna 404 si ID no existe     |

## 🚀 Instalación y Configuración

### 1. Clonar y activar entorno

```bash
# Activar entorno virtual
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Aplicar migraciones

```bash
python manage.py migrate
```

### 4. Crear superusuario

```bash
python manage.py createsuperuser
# Usuario: admin
# Password: admin123
```

### 5. Cargar datos de ejemplo

```bash
python manage.py shell
# En el shell:
from miapp.models import Order
from decimal import Decimal
Order.objects.create(
    customer_name="Juan Pérez",
    customer_email="juan@example.com",
    product_name="Laptop Dell XPS",
    quantity=1,
    total_amount=Decimal("1299.99"),
    status="Confirmado"
)
```

### 6. Iniciar servidor de desarrollo

```bash
python manage.py runserver
```

Accede a:

- Frontend: http://localhost:8000/orders/
- Admin: http://localhost:8000/admin/

## 📁 Estructura del Proyecto

```
proyecto_web/
├── manage.py
├── README.md
├── requirements.txt
├── db.sqlite3
├── proyecto_web_inicial/
│   ├── settings.py      # Configuración (miapp en INSTALLED_APPS)
│   ├── urls.py          # URLs principales con include()
│   ├── wsgi.py
│   └── asgi.py
└── miapp/
    ├── models.py        # Modelo Order
    ├── views.py         # Vistas: order_list, order_detail
    ├── urls.py          # URLs de miapp
    ├── admin.py         # Admin registrado con fields
    ├── migrations/
    │   ├── 0001_initial.py
    │   └── __init__.py
    └── templates/miapp/
        ├── base.html           # Template base
        ├── order_list.html     # Listado de órdenes
        └── order_detail.html   # Detalle de orden
```

## 🛠️ Comandos Principales

### Crear migraciones

```bash
python manage.py makemigrations
```

### Aplicar migraciones

```bash
python manage.py migrate
```

### Acceder a Django Shell

```bash
python manage.py shell
```

### Ejecutar servidor

```bash
python manage.py runserver 8000
```

### Ver órdenes en shell

```bash
python manage.py shell
>>> from miapp.models import Order
>>> Order.objects.all()
>>> Order.objects.get(id=1)
>>> Order.objects.filter(status='Confirmado')
```

## 👤 Credenciales de Admin

- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **URL:** `http://localhost:8000/admin/`

## 📊 Datos de Ejemplo

El proyecto incluye 4 pedidos de prueba:

1. Juan Pérez - Laptop Dell XPS - Confirmado - $1,299.99
2. María García - Monitor LG 27" - Pendiente - $798.00
3. Carlos López - Teclado Mecánico - Confirmado - $450.00
4. Ana Martínez - Ratón Logitech - Enviado - $299.95

## ✅ Validaciones Implementadas

- [x] miapp registrada en INSTALLED_APPS
- [x] Modelo Order con 8 campos (más de 4 requeridos)
- [x] Migraciones aplicadas
- [x] Order registrado en admin.py con lista de campos
- [x] Superusuario creado
- [x] Varios pedidos creados
- [x] Vista order_list funcionando
- [x] Vista order_detail funcionando
- [x] miapp/urls.py creado
- [x] urls.py principal conectado con include()
- [x] base.html creado
- [x] order_list.html creado
- [x] order_detail.html creado
- [x] /orders/ devuelve listado (200 OK)
- [x] /orders/1/ devuelve detalle (200 OK)
- [x] /orders/999/ devuelve 404 Not Found

## 🔗 Tecnologías Utilizadas

- **Django:** 6.0.5
- **Python:** 3.14+
- **Database:** SQLite3
- **Frontend:** HTML + Django Templates

## 📝 Notas

- El sistema utiliza `get_object_or_404()` para manejo robusto de IDs inexistentes
- Los templates heredan de `base.html` siguiendo buenas prácticas
- Django Admin está completamente configurado para gestión de pedidos
- La base de datos SQLite es perfecta para desarrollo local

## 🎓 Conceptos Aprendidos

1. Modelos Django y ORM
2. Django Admin y ModelAdmin
3. Vistas basadas en funciones
4. URLs y enrutamiento
5. Templates y herencia de templates
6. Migraciones de base de datos
7. Manejo de errores HTTP (404)
8. get_object_or_404() para queries seguras

---

**Estado:** ✅ Proyecto completado y validado
**Última actualización:** Mayo 2026
