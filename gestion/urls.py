from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register(
    r'api/productos',
    views.ProductoViewSet
)

router.register(
    r'api/movimientos',
    views.MovimientoViewSet
)

router.register(
    r'api/categorias',
    views.CategoriaViewSet
)


urlpatterns = [

    # Dashboard
    path(
        '',
        views.resumen,
        name='resumen'
    ),

    # Productos
    path(
        'productos/',
        views.productos,
        name='productos'
    ),

    path(
        'productos/nuevo/',
        views.producto_nuevo,
        name='producto_nuevo'
    ),

    path(
        'productos/<int:producto_id>/editar/',
        views.producto_editar,
        name='producto_editar'
    ),

    # Movimientos
    path(
        'movimientos/',
        views.movimientos,
        name='movimientos'
    ),

    path(
        'movimientos/nuevo/',
        views.movimiento_nuevo,
        name='movimiento_nuevo'
    ),

    # Solicitudes
    path(
        'solicitudes/',
        views.solicitudes,
        name='solicitudes'
    ),

    path(
        'solicitudes/nueva/',
        views.solicitud_nueva,
        name='solicitud_nueva'
    ),

    # API REST
    path(
        '',
        include(router.urls)
    ),
]