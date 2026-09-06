# Sistema de Inventario Full Stack

Aplicación web para gestionar productos, categorías, movimientos de inventario y solicitudes internas.

## Tecnologías

- Django 5.2.1
- Django REST Framework
- SQLite para desarrollo local
- Plantillas HTML y CSS

## Funcionalidades

- Dashboard de inventario.
- Control de stock mínimo.
- Creación y edición de productos.
- Registro de entradas y salidas.
- Validación de stock insuficiente.
- Módulo de solicitudes.
- API REST para productos, movimientos y categorías.
- Pruebas automáticas.

## Instalación local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

Antes de publicar una instancia real, configura una clave secreta propia, `DJANGO_DEBUG=False`, los hosts permitidos y el número de soporte de WhatsApp.

## Pruebas

```powershell
python manage.py test
```
