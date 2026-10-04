from django.test import Client, TestCase
from django.urls import reverse
from .models import Contacto


class ContactoTests(TestCase):
    def setUp(self):
        self.url = reverse('contacto:contacto_formulario')
        self.datos = {'nombre': 'Mauro', 'email': 'prueba@example.com', 'mensaje': 'Quisiera consultar por un perfume.'}

    def test_formulario_y_enlace(self):
        self.assertContains(self.client.get(self.url), 'Enviar consulta')
        self.assertContains(self.client.get(reverse('lista_perfumes')), 'href="/contacto/"')

    def test_envio_valido_y_campos_protegidos(self):
        response = self.client.post(self.url, self.datos | {'atendido': 'on'})
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        contacto = Contacto.objects.get()
        self.assertFalse(contacto.atendido)
        self.assertEqual(contacto.telefono, '')
        self.assertContains(self.client.get(self.url), 'Tu consulta quedó registrada correctamente.')
        self.assertEqual(Contacto.objects.count(), 1)

    def test_invalidos_no_guardan(self):
        for cambio in ({'nombre': ''}, {'email': 'invalido'}, {'mensaje': 'corto'}):
            with self.subTest(cambio=cambio):
                response = self.client.post(self.url, self.datos | cambio)
                self.assertTrue(response.context['form'].errors)
                self.assertFalse(Contacto.objects.exists())

    def test_csrf(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(self.url, self.datos).status_code, 403)
        self.assertFalse(Contacto.objects.exists())
        client.get(self.url)
        token = client.cookies['csrftoken'].value
        self.assertEqual(client.post(self.url, self.datos | {'csrfmiddlewaretoken': token}).status_code, 302)
        self.assertEqual(Contacto.objects.count(), 1)
