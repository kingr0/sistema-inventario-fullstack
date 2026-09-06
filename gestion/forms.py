from django import forms
from .models import MovimientoInventario, ProductoBodega, Solicitud


class MovimientoForm(forms.ModelForm):

    tipo = forms.ChoiceField(
        choices=[
            ('ENTRADA', 'Entrada'),
            ('SALIDA', 'Salida')
        ],
        label='Tipo'
    )

    class Meta:
        model = MovimientoInventario
        fields = [
            'producto',
            'tipo',
            'cantidad',
            'responsable',
            'observacion'
        ]

        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'responsable': 'Responsable',
            'observacion': 'Observación',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['producto'].queryset = ProductoBodega.objects.filter(
            activo=True
        ).order_by('codigo')

    def clean(self):
        cleaned_data = super().clean()

        producto = cleaned_data.get('producto')
        tipo = cleaned_data.get('tipo')
        cantidad = cleaned_data.get('cantidad')

        if producto and tipo == 'SALIDA' and cantidad:

            if cantidad > producto.stock_actual:
                raise forms.ValidationError(
                    f'Stock insuficiente. '
                    f'El producto tiene {producto.stock_actual} unidades disponibles.'
                )

        return cleaned_data


class ProductoForm(forms.ModelForm):

    class Meta:
        model = ProductoBodega

        fields = [
            'codigo',
            'nombre',
            'categoria',
            'stock_actual',
            'stock_minimo',
            'activo'
        ]

        labels = {
            'codigo': 'Código',
            'nombre': 'Nombre',
            'categoria': 'Categoría',
            'stock_actual': 'Stock actual',
            'stock_minimo': 'Stock mínimo',
            'activo': 'Producto activo',
        }


class SolicitudForm(forms.ModelForm):

    class Meta:
        model = Solicitud

        fields = [
            'titulo',
            'descripcion',
            'prioridad'
        ]

        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'prioridad': 'Prioridad',
        }