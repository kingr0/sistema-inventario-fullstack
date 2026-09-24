from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


router = DefaultRouter()

router.register(
    r'api/v1/productos',
    views.ProductoViewSet
)

router.register(
    r'api/v1/movimientos',
    views.MovimientoViewSet
)

router.register(
    r'api/v1/categorias',
    views.CategoriaViewSet
)

router.register(
    r'api/v1/solicitudes',
    views.SolicitudViewSet
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

    # Documentación de la API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]