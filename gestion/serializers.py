from rest_framework import serializers
from django.db import transaction

from .models import (
    ProductoBodega,
    MovimientoInventario,
    CategoriaInsumo
)


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoriaInsumo
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):

    stock_bajo = serializers.ReadOnlyField()

    class Meta:
        model = ProductoBodega
        fields = '__all__'


class MovimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovimientoInventario
        fields = '__all__'
        read_only_fields = ['fecha']

    def validate(self, data):

        producto = data.get('producto')
        tipo = data.get('tipo')
        cantidad = data.get('cantidad')

        if cantidad is not None and cantidad <= 0:
            raise serializers.ValidationError(
                'La cantidad debe ser mayor a 0.'
            )

        if (
            producto
            and tipo == 'SALIDA'
            and cantidad
            and cantidad > producto.stock_actual
        ):
            raise serializers.ValidationError({
                'cantidad':
                    f'Stock insuficiente. '
                    f'Hay {producto.stock_actual} unidades disponibles.'
            })

        return data

    @transaction.atomic
    def create(self, validated_data):

        producto = validated_data['producto']
        tipo = validated_data['tipo']
        cantidad = validated_data['cantidad']

        producto = ProductoBodega.objects.select_for_update().get(
            pk=producto.pk
        )

        if tipo == 'ENTRADA':
            producto.stock_actual += cantidad

        elif tipo == 'SALIDA':

            if cantidad > producto.stock_actual:
                raise serializers.ValidationError({
                    'cantidad': 'Stock insuficiente.'
                })

            producto.stock_actual -= cantidad

        producto.save()

        movimiento = MovimientoInventario.objects.create(
            producto=producto,
            tipo=tipo,
            cantidad=cantidad,
            responsable=validated_data.get(
                'responsable',
                ''
            ),
            observacion=validated_data.get(
                'observacion',
                ''
            )
        )

        return movimiento