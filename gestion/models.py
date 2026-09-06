from django.db import models
from django.contrib.auth.models import User


class CategoriaInsumo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class ProductoBodega(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=200)
    stock_actual = models.PositiveIntegerField(default=0)

    # NUEVAS MEJORAS
    stock_minimo = models.PositiveIntegerField(default=5)
    activo = models.BooleanField(default=True)

    categoria = models.ForeignKey(
        CategoriaInsumo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def stock_bajo(self):
        return self.stock_actual <= self.stock_minimo

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['codigo']


class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida')
    ]

    producto = models.ForeignKey(
        ProductoBodega,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES
    )

    cantidad = models.PositiveIntegerField()

    responsable = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    observacion = models.TextField(blank=True)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-fecha']


class Solicitud(models.Model):

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
        ('COMPLETADA', 'Completada'),
    ]

    PRIORIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
    ]

    titulo = models.CharField(max_length=200)

    descripcion = models.TextField()

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    fecha_actualizacion = models.DateTimeField(auto_now=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE'
    )

    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='MEDIA'
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='solicitudes'
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
        ordering = ['-fecha_creacion']