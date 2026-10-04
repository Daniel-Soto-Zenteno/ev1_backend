from django.test import TestCase
from django.urls import reverse

from .models import Contacto


class ContactoModelTest(TestCase):
    def test_crear_contacto(self):
        contacto = Contacto.objects.create(
            nombre="Juan Pérez",
            email="juan@example.com",
            mensaje="Hola, quisiera más información.",
        )
        self.assertEqual(str(contacto).startswith("Juan Pérez"), True)
        self.assertFalse(contacto.atendido)


class ContactoViewTest(TestCase):
    def test_get_formulario(self):
        response = self.client.get(reverse("contacto:formulario"))
        self.assertEqual(response.status_code, 200)

    def test_post_formulario_valido(self):
        data = {
            "nombre": "Ana Torres",
            "email": "ana@example.com",
            "telefono": "",
            "asunto": "Consulta",
            "mensaje": "¿Tienen disponibilidad?",
        }
        response = self.client.post(reverse("contacto:formulario"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contacto.objects.count(), 1)