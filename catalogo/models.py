from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models


class Perfume(models.Model):
    class Categoria(models.TextChoices):
        FEMENINO = 'Femenino', 'Femenino'
        MASCULINO = 'Masculino', 'Masculino'
        UNISEX = 'Unisex', 'Unisex'

    nombre = models.CharField(max_length=120)
    categoria = models.CharField('categoría', max_length=10, choices=Categoria.choices)
    precio = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(1)])
    ml = models.PositiveIntegerField('formato en ml', validators=[MinValueValidator(1)])
    en_stock = models.BooleanField('disponible', default=True)
    destacado = models.BooleanField(default=False)
    imagen = models.ImageField('imagen', upload_to='perfumes/', blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre', 'pk']

    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        self.nombre = self.nombre.strip()
        errores = {}
        if len(self.nombre) < 3:
            errores['nombre'] = 'El nombre del perfume debe tener al menos 3 caracteres.'
        if self.destacado and not self.en_stock:
            errores['destacado'] = 'Solo se pueden destacar perfumes disponibles para la venta.'
        if errores:
            raise ValidationError(errores)
