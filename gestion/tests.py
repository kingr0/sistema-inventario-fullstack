from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from .models import (
    CategoriaInsumo,
    ProductoBodega,
    MovimientoInventario,
    Solicitud
)


class ProductoAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_superuser(
            'testadmin',
            '',
            'testpass'
        )

        self.client.force_authenticate(user=self.user)

        self.categoria = CategoriaInsumo.objects.create(
            nombre='Materiales de aseo'
        )

        self.producto = ProductoBodega.objects.create(
            codigo='ASE-001',
            nombre='Alcohol gel 1 litro',
            stock_actual=10,
            stock_minimo=5,
            activo=True,
            categoria=self.categoria
        )

    def test_listar_productos(self):
        response = self.client.get('/api/productos/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_crear_producto(self):

        data = {
            'codigo': 'ASE-999',
            'nombre': 'Producto de prueba',
            'stock_actual': 5,
            'stock_minimo': 3,
            'activo': True,
            'categoria': self.categoria.id
        }

        response = self.client.post(
            '/api/productos/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            ProductoBodega.objects.filter(
                codigo='ASE-999'
            ).exists()
        )

    def test_obtener_producto(self):

        response = self.client.get(
            f'/api/productos/{self.producto.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['nombre'],
            'Alcohol gel 1 litro'
        )

    def test_eliminar_producto(self):

        response = self.client.delete(
            f'/api/productos/{self.producto.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_detectar_stock_bajo(self):

        self.producto.stock_actual = 3
        self.producto.stock_minimo = 5
        self.producto.save()

        self.assertTrue(
            self.producto.stock_bajo
        )


class MovimientoAPITest(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create_superuser(
            'testadmin2',
            '',
            'testpass'
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.categoria = CategoriaInsumo.objects.create(
            nombre='Materiales de aseo'
        )

        self.producto = ProductoBodega.objects.create(
            codigo='ASE-001',
            nombre='Alcohol gel 1 litro',
            stock_actual=10,
            stock_minimo=5,
            activo=True,
            categoria=self.categoria
        )

    def test_listar_movimientos(self):

        response = self.client.get(
            '/api/movimientos/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_entrada_aumenta_stock(self):

        data = {
            'producto': self.producto.id,
            'tipo': 'ENTRADA',
            'cantidad': 5,
            'responsable': 'Test',
            'observacion': 'Prueba de entrada'
        }

        response = self.client.post(
            '/api/movimientos/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.producto.refresh_from_db()

        self.assertEqual(
            self.producto.stock_actual,
            15
        )

    def test_salida_disminuye_stock(self):

        data = {
            'producto': self.producto.id,
            'tipo': 'SALIDA',
            'cantidad': 4,
            'responsable': 'Test',
            'observacion': 'Prueba de salida'
        }

        response = self.client.post(
            '/api/movimientos/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.producto.refresh_from_db()

        self.assertEqual(
            self.producto.stock_actual,
            6
        )

    def test_no_permitir_salida_mayor_al_stock(self):

        data = {
            'producto': self.producto.id,
            'tipo': 'SALIDA',
            'cantidad': 20,
            'responsable': 'Test',
            'observacion': 'Intento de salida inválida'
        }

        response = self.client.post(
            '/api/movimientos/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.producto.refresh_from_db()

        self.assertEqual(
            self.producto.stock_actual,
            10
        )


class CategoriaAPITest(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create_superuser(
            'testadmin3',
            '',
            'testpass'
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_listar_categorias(self):

        response = self.client.get(
            '/api/categorias/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_crear_categoria(self):

        data = {
            'nombre': 'Nueva categoria',
            'descripcion': ''
        }

        response = self.client.post(
            '/api/categorias/',
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


class SolicitudTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='usuario_prueba',
            password='testpass'
        )

    def test_crear_solicitud(self):

        solicitud = Solicitud.objects.create(
            titulo='Solicitud de insumos',
            descripcion='Se necesitan nuevos insumos',
            prioridad='ALTA',
            usuario=self.user
        )

        self.assertEqual(
            solicitud.estado,
            'PENDIENTE'
        )

        self.assertEqual(
            solicitud.prioridad,
            'ALTA'
        )