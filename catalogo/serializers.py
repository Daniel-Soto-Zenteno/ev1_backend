from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Perfume


class PerfumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfume
        fields = [
            'id', 'nombre', 'categoria', 'precio', 'ml',
            'en_stock', 'destacado', 'imagen', 'creado',
        ]
        read_only_fields = ['id', 'creado']

    def validate(self, attrs):
        # En una edición parcial, validar también los datos actuales del perfume.
        candidato = Perfume()
        if self.instance is not None:
            for field in Perfume._meta.concrete_fields:
                setattr(candidato, field.attname, getattr(self.instance, field.attname))
        for nombre, valor in attrs.items():
            setattr(candidato, nombre, valor)

        # ModelSerializer no ejecuta Model.clean() automáticamente.
        try:
            candidato.clean()
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.message_dict) from error

        if 'nombre' in attrs:
            attrs['nombre'] = candidato.nombre
        return attrs
