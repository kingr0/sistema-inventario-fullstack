from rest_framework import serializers
from django.db import transaction

from .models import (
    ProductoBodega,
    MovimientoInventario,
    CategoriaInsumo,
    Solicitud
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

        try:
            producto.aplicar_movimiento(tipo, cantidad)
        except ValueError as e:
            raise serializers.ValidationError({'cantidad': str(e)})

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

    @transaction.atomic
    def update(self, instance, validated_data):

        producto_anterior = ProductoBodega.objects.select_for_update().get(
            pk=instance.producto.pk
        )

        # 1. Revertir el efecto del movimiento ANTERIOR
        producto_anterior.revertir_movimiento(
            instance.tipo,
            instance.cantidad
        )

        # 2. Aplicar el efecto del movimiento NUEVO (con los datos actualizados)
        producto_nuevo = validated_data.get('producto', instance.producto)
        tipo_nuevo = validated_data.get('tipo', instance.tipo)
        cantidad_nueva = validated_data.get('cantidad', instance.cantidad)

        producto_nuevo = ProductoBodega.objects.select_for_update().get(
            pk=producto_nuevo.pk
        )

        try:
            producto_nuevo.aplicar_movimiento(tipo_nuevo, cantidad_nueva)
        except ValueError as e:
            raise serializers.ValidationError({'cantidad': str(e)})

        # 3. Actualizar los campos del movimiento
        instance.producto = producto_nuevo
        instance.tipo = tipo_nuevo
        instance.cantidad = cantidad_nueva
        instance.responsable = validated_data.get('responsable', instance.responsable)
        instance.observacion = validated_data.get('observacion', instance.observacion)
        instance.save()

        return instance


class SolicitudSerializer(serializers.ModelSerializer):

    usuario = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Solicitud
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'usuario']

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)