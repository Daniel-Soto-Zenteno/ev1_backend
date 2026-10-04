from django import forms
from .models import Perfume


class PerfumeForm(forms.ModelForm):
    class Meta:
        model = Perfume
        fields = ['nombre', 'categoria', 'precio', 'ml', 'en_stock', 'destacado']
        help_texts = {
            'precio': 'Precio en pesos chilenos, mayor que cero.',
            'ml': 'Capacidad del frasco en mililitros, mayor que cero.',
        }
