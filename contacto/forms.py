from django import forms
from .models import Contacto


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'telefono', 'asunto', 'mensaje']
        widgets = {'mensaje': forms.Textarea(attrs={'rows': 5})}
        help_texts = {'telefono': 'Opcional.', 'asunto': 'Opcional.', 'mensaje': 'Escribe al menos 10 caracteres.'}

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 2:
            raise forms.ValidationError('Escribe un nombre de al menos 2 caracteres.')
        return nombre

    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje'].strip()
        if len(mensaje) < 10:
            raise forms.ValidationError('El mensaje debe tener al menos 10 caracteres.')
        return mensaje
