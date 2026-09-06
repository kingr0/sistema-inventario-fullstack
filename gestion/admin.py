from django.contrib import admin
from .models import CategoriaInsumo, ProductoBodega, MovimientoInventario, Solicitud

admin.site.register(CategoriaInsumo)
admin.site.register(ProductoBodega)
admin.site.register(MovimientoInventario)
admin.site.register(Solicitud)
