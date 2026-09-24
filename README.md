# Sistema de Inventario de Bodega

Sistema web para la gestión de inventario de bodega: productos, movimientos de stock (entradas/salidas), categorías y solicitudes de insumos. Incluye una interfaz web y una API REST documentada.

## Tecnologías

- **Backend:** Django + Django REST Framework
- **Base de datos:** SQLite (desarrollo)
- **Autenticación API:** Token Authentication
- **Documentación API:** Swagger / OpenAPI (drf-spectacular)
- **Filtros y búsqueda:** django-filter

## Requisitos previos

- Python 3.10 o superior
- pip

## Instalación

1. Clona el repositorio y entra a la carpeta:
   ```bash
   git clone https://github.com/kingr0/sistema-inventario-fullstack.git
   cd sistema-inventario-fullstack
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Mac/Linux
   source .venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Copia `.env.example` como `.env` en la raíz del proyecto (mismo nivel que `manage.py`) y configura tus valores locales:
   ```
   SECRET_KEY=tu-clave-secreta-aqui
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   WHATSAPP_SUPPORT_NUMBER=
   ```

   Para generar una `SECRET_KEY` segura:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   El soporte por WhatsApp queda oculto si no se configura un número. Para habilitarlo, utiliza un número de soporte autorizado en formato internacional, solo dígitos. Ese número será visible para quienes usen la aplicación; no guardes un contacto privado en el código.

5. Aplica las migraciones:
   ```bash
   python manage.py migrate
   ```

6. Crea un usuario administrador:
   ```bash
   python manage.py createsuperuser
   ```

7. Genera un token de autenticación para tu usuario (necesario para usar la API):
   ```bash
   python manage.py drf_create_token tu_usuario
   ```

## Ejecución

```bash
python manage.py runserver
```

El sistema queda disponible en: `http://127.0.0.1:8000/`

## Usuarios y accesos

- **Interfaz web:** requiere iniciar sesión como staff (`/admin/login/`)
- **API REST:** requiere un token de autenticación, enviado en el header:
  ```
  Authorization: Token <tu_token>
  ```

## Documentación interactiva de la API

Con el servidor corriendo, la documentación completa (Swagger UI) está disponible en:

```
http://127.0.0.1:8000/api/docs/
```

Ahí se pueden ver y probar todos los endpoints disponibles.

## Endpoints principales de la API

Todas las rutas están bajo el prefijo `/api/v1/` y requieren autenticación por token.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/productos/` | Lista productos (paginado, 20 por página) |
| GET | `/api/v1/productos/?search=texto` | Busca productos por nombre o código |
| GET | `/api/v1/productos/?categoria=<id>` | Filtra productos por categoría |
| GET | `/api/v1/productos/?activo=true` | Filtra productos activos/inactivos |
| POST | `/api/v1/productos/` | Crea un producto |
| GET | `/api/v1/productos/<id>/` | Detalle de un producto |
| PUT/PATCH | `/api/v1/productos/<id>/` | Edita un producto |
| DELETE | `/api/v1/productos/<id>/` | Elimina un producto |
| GET | `/api/v1/movimientos/` | Lista movimientos de stock |
| POST | `/api/v1/movimientos/` | Registra una entrada o salida de stock |
| PUT/PATCH | `/api/v1/movimientos/<id>/` | Edita un movimiento (recalcula el stock automáticamente) |
| DELETE | `/api/v1/movimientos/<id>/` | Elimina un movimiento (revierte el stock automáticamente) |
| GET | `/api/v1/categorias/` | Lista categorías |
| POST | `/api/v1/categorias/` | Crea una categoría |
| GET | `/api/v1/solicitudes/` | Lista solicitudes |
| POST | `/api/v1/solicitudes/` | Crea una solicitud (el usuario se asigna automáticamente) |

## Ejemplos de uso (curl)

**Listar productos:**
```bash
curl http://127.0.0.1:8000/api/v1/productos/ -H "Authorization: Token TU_TOKEN"
```

**Registrar una entrada de stock:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/movimientos/ \
  -H "Authorization: Token TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"producto": 1, "tipo": "ENTRADA", "cantidad": 10}'
```

## Pruebas automatizadas

El proyecto incluye pruebas unitarias que cubren autenticación, permisos, y la lógica de entradas/salidas/edición/eliminación de movimientos.

Para ejecutarlas:
```bash
python manage.py test gestion
```

## Notas de seguridad

- La `SECRET_KEY` y las variables sensibles se gestionan mediante un archivo `.env` (no incluido en el repositorio).
- No publiques tokens, contraseñas, archivos `.env`, bases de datos locales ni capturas que muestren credenciales. La base de datos y los usuarios se crean localmente con las migraciones y `createsuperuser`.
- Los valores de `.env.example` son ejemplos; genera una clave propia antes de ejecutar el sistema. Esta configuración de desarrollo no constituye una certificación de seguridad para producción.
- En producción, se debe establecer `DEBUG=False`, lo que activa automáticamente HTTPS forzado, cookies seguras y HSTS.
- Verificar la configuración de seguridad con:
  ```bash
  python manage.py check --deploy
  ```
