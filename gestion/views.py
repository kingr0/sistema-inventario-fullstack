from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Q, F

from .models import (
    ProductoBodega,
    MovimientoInventario,
    CategoriaInsumo,
    Solicitud
)

from .forms import (
    MovimientoForm,
    ProductoForm,
    SolicitudForm
)

from rest_framework import viewsets

from .serializers import (
    ProductoSerializer,
    MovimientoSerializer,
    CategoriaSerializer
)


# ============================================================
# RESUMEN GENERAL
# ============================================================

@staff_member_required(login_url='/admin/login/')
def resumen(request):

    total_productos = ProductoBodega.objects.filter(
        activo=True
    ).count()

    total_categorias = CategoriaInsumo.objects.count()

    stock_total = ProductoBodega.objects.filter(
        activo=True
    ).aggregate(
        t=Sum('stock_actual')
    )['t'] or 0


    # --------------------------------------------------------
    # PRODUCTOS CON STOCK BAJO
    # Compara stock_actual con stock_minimo de cada producto
    # --------------------------------------------------------

    productos_stock_bajo = ProductoBodega.objects.filter(
        activo=True,
        stock_actual__lte=F('stock_minimo')
    )

    total_stock_bajo = productos_stock_bajo.count()


    # --------------------------------------------------------
    # SOLICITUDES PENDIENTES
    # --------------------------------------------------------

    solicitudes_pendientes = Solicitud.objects.filter(
        estado='PENDIENTE'
    ).count()


    # --------------------------------------------------------
    # RESUMEN POR CATEGORÍA
    # --------------------------------------------------------

    resumen_categorias = []

    for cat in CategoriaInsumo.objects.all():

        prods = ProductoBodega.objects.filter(
            categoria=cat,
            activo=True
        )

        stock = prods.aggregate(
            t=Sum('stock_actual')
        )['t'] or 0

        resumen_categorias.append({
            'nombre': cat.nombre,
            'productos': prods.count(),
            'stock': stock
        })


    # --------------------------------------------------------
    # ÚLTIMOS MOVIMIENTOS
    # --------------------------------------------------------

    ultimos_movimientos = MovimientoInventario.objects.select_related(
        'producto'
    ).order_by('-fecha')[:10]


    return render(
        request,
        'gestion/resumen.html',
        {
            'total_productos': total_productos,
            'total_categorias': total_categorias,
            'stock_total': stock_total,

            'total_stock_bajo': total_stock_bajo,
            'productos_stock_bajo': productos_stock_bajo[:5],

            'solicitudes_pendientes': solicitudes_pendientes,

            'resumen_categorias': resumen_categorias,

            'ultimos_movimientos': ultimos_movimientos,
        }
    )


# ============================================================
# PRODUCTOS
# ============================================================

@staff_member_required(login_url='/admin/login/')
def productos(request):

    q = request.GET.get('q', '')

    categoria_id = request.GET.get(
        'categoria',
        ''
    )


    productos_qs = ProductoBodega.objects.select_related(
        'categoria'
    ).order_by('codigo')


    # --------------------------------------------------------
    # BÚSQUEDA POR NOMBRE O CÓDIGO
    # --------------------------------------------------------

    if q:

        productos_qs = productos_qs.filter(

            Q(nombre__icontains=q) |

            Q(codigo__icontains=q)

        )


    # --------------------------------------------------------
    # FILTRO POR CATEGORÍA
    # --------------------------------------------------------

    if categoria_id:

        productos_qs = productos_qs.filter(
            categoria_id=categoria_id
        )


    categorias = CategoriaInsumo.objects.all()


    return render(
        request,
        'gestion/productos.html',
        {
            'productos': productos_qs,
            'categorias': categorias,
            'q': q,
            'categoria_id': categoria_id,
        }
    )


# ============================================================
# NUEVO PRODUCTO
# ============================================================

@staff_member_required(login_url='/admin/login/')
def producto_nuevo(request):

    if request.method == 'POST':

        form = ProductoForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Producto creado correctamente.'
            )

            return redirect(
                'productos'
            )

    else:

        form = ProductoForm()


    return render(
        request,
        'gestion/producto_form.html',
        {
            'form': form,
            'titulo': 'Nuevo producto'
        }
    )


# ============================================================
# EDITAR PRODUCTO
# ============================================================

@staff_member_required(login_url='/admin/login/')
def producto_editar(
    request,
    producto_id
):

    producto = get_object_or_404(
        ProductoBodega,
        id=producto_id
    )


    if request.method == 'POST':

        form = ProductoForm(
            request.POST,
            instance=producto
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Producto actualizado correctamente.'
            )

            return redirect(
                'productos'
            )

    else:

        form = ProductoForm(
            instance=producto
        )


    return render(
        request,
        'gestion/producto_form.html',
        {
            'form': form,
            'titulo': 'Editar producto'
        }
    )


# ============================================================
# MOVIMIENTOS
# ============================================================

@staff_member_required(login_url='/admin/login/')
def movimientos(request):

    movimientos_qs = MovimientoInventario.objects.select_related(
        'producto'
    ).order_by(
        '-fecha'
    )[:50]


    return render(
        request,
        'gestion/movimientos.html',
        {
            'movimientos': movimientos_qs
        }
    )


# ============================================================
# NUEVO MOVIMIENTO
# ============================================================

@staff_member_required(login_url='/admin/login/')
def movimiento_nuevo(request):

    if request.method == 'POST':

        form = MovimientoForm(
            request.POST
        )


        if form.is_valid():

            mov = form.save(
                commit=False
            )

            producto = mov.producto


            # ------------------------------------------------
            # ENTRADA DE INVENTARIO
            # ------------------------------------------------

            if mov.tipo == 'ENTRADA':

                producto.stock_actual += mov.cantidad


            # ------------------------------------------------
            # SALIDA DE INVENTARIO
            # ------------------------------------------------

            elif mov.tipo == 'SALIDA':

                producto.stock_actual -= mov.cantidad


            producto.save()

            mov.save()


            messages.success(
                request,
                'Movimiento registrado correctamente.'
            )


            return redirect(
                'resumen'
            )


    else:

        form = MovimientoForm()


    return render(
        request,
        'gestion/movimiento_form.html',
        {
            'form': form
        }
    )


# ============================================================
# SOLICITUDES
# ============================================================

@staff_member_required(login_url='/admin/login/')
def solicitudes(request):

    solicitudes_qs = Solicitud.objects.select_related(
        'usuario'
    ).order_by(
        '-fecha_creacion'
    )


    return render(
        request,
        'gestion/solicitudes.html',
        {
            'solicitudes': solicitudes_qs
        }
    )


# ============================================================
# NUEVA SOLICITUD
# ============================================================

@staff_member_required(login_url='/admin/login/')
def solicitud_nueva(request):

    if request.method == 'POST':

        form = SolicitudForm(
            request.POST
        )

        if form.is_valid():

            solicitud = form.save(
                commit=False
            )

            solicitud.usuario = request.user

            solicitud.save()


            messages.success(
                request,
                'Solicitud creada correctamente.'
            )


            return redirect(
                'solicitudes'
            )


    else:

        form = SolicitudForm()


    return render(
        request,
        'gestion/solicitud_form.html',
        {
            'form': form
        }
    )


# ============================================================
# API REST - CATEGORÍAS
# ============================================================

class CategoriaViewSet(
    viewsets.ModelViewSet
):

    queryset = CategoriaInsumo.objects.all()

    serializer_class = CategoriaSerializer


# ============================================================
# API REST - PRODUCTOS
# ============================================================

class ProductoViewSet(
    viewsets.ModelViewSet
):

    queryset = ProductoBodega.objects.all().order_by(
        'codigo'
    )

    serializer_class = ProductoSerializer


# ============================================================
# API REST - MOVIMIENTOS
# ============================================================

class MovimientoViewSet(
    viewsets.ModelViewSet
):

    queryset = MovimientoInventario.objects.all().order_by(
        '-fecha'
    )

    serializer_class = MovimientoSerializer