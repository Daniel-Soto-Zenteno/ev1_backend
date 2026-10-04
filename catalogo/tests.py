from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from .models import Perfume


class PerfumeCrudTests(TestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(username='administrador', password='test-only', is_staff=True)
        self.datos = {'nombre': 'Citrus Fresh', 'categoria': 'Unisex', 'precio': '12000', 'ml': '50', 'en_stock': 'on'}
        self.perfume = Perfume.objects.create(nombre='Dulce Noche', categoria='Femenino', precio=15000, ml=100)
        self.client.force_login(self.staff)

    def test_listado_publico(self):
        self.client.logout()
        response = self.client.get(reverse('lista_perfumes'))
        self.assertContains(response, 'Dulce Noche')
        self.assertNotContains(response, 'Agregar perfume')

    def test_creacion_valida(self):
        response = self.client.post(reverse('perfume_crear'), self.datos)
        self.assertRedirects(response, reverse('lista_perfumes'))
        self.assertTrue(Perfume.objects.filter(nombre='Citrus Fresh').exists())

    def test_datos_invalidos_no_guardan(self):
        for cambios in ({'nombre': ''}, {'nombre': '  '}, {'precio': '0'}, {'precio': '-1'}, {'ml': '0'}, {'categoria': 'Otra'}, {'en_stock': '', 'destacado': 'on'}):
            with self.subTest(cambios=cambios):
                response = self.client.post(reverse('perfume_crear'), self.datos | cambios)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context['form'].errors)
                self.assertEqual(Perfume.objects.count(), 1)

    def test_edicion_precargada_y_guardada(self):
        url = reverse('perfume_editar', args=[self.perfume.pk])
        response = self.client.get(url)
        self.assertEqual(response.context['form'].instance.pk, self.perfume.pk)
        self.assertRedirects(self.client.post(url, self.datos), reverse('lista_perfumes'))
        self.perfume.refresh_from_db()
        self.assertEqual(self.perfume.nombre, 'Citrus Fresh')

    def test_eliminacion_solo_post_y_cancelacion(self):
        url = reverse('perfume_eliminar', args=[self.perfume.pk])
        self.assertContains(self.client.get(url), 'Confirmar eliminación')
        self.client.get(reverse('lista_perfumes'))
        self.assertTrue(Perfume.objects.filter(pk=self.perfume.pk).exists())
        self.assertRedirects(self.client.post(url), reverse('lista_perfumes'))
        self.assertFalse(Perfume.objects.filter(pk=self.perfume.pk).exists())

    def test_id_inexistente_404(self):
        for nombre in ('perfume_editar', 'perfume_eliminar'):
            self.assertEqual(self.client.get(reverse(nombre, args=[99999])).status_code, 404)

    def test_visitantes_y_usuarios_sin_permiso_no_modifican(self):
        usuario = get_user_model().objects.create_user(username='cliente', password='test-only')
        for autenticado in (False, True):
            if autenticado:
                self.client.force_login(usuario)
            else:
                self.client.logout()
            for url in (reverse('perfume_crear'), reverse('perfume_editar', args=[self.perfume.pk]), reverse('perfume_eliminar', args=[self.perfume.pk])):
                self.assertEqual(self.client.post(url, self.datos).status_code, 302)
        self.assertEqual(Perfume.objects.count(), 1)
        self.perfume.refresh_from_db()
        self.assertEqual(self.perfume.nombre, 'Dulce Noche')

    def test_csrf_rechaza_y_acepta_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.staff)
        url = reverse('perfume_crear')
        self.assertEqual(client.post(url, self.datos).status_code, 403)
        self.assertEqual(Perfume.objects.count(), 1)
        client.get(url)
        token = client.cookies['csrftoken'].value
        self.assertEqual(client.post(url, self.datos | {'csrfmiddlewaretoken': token}).status_code, 302)
        eliminar = reverse('perfume_eliminar', args=[self.perfume.pk])
        self.assertEqual(client.post(eliminar).status_code, 403)
        self.assertTrue(Perfume.objects.filter(pk=self.perfume.pk).exists())
        self.assertEqual(client.post(eliminar, {'csrfmiddlewaretoken': token}).status_code, 302)

    def test_nosotros_y_admin(self):
        self.assertContains(self.client.get(reverse('historia_y_guia')), 'Calbuco')
        self.assertContains(self.client.get(reverse('historia_y_guia')), 'Cuida tu perfume')
        from django.contrib import admin
        self.assertIn(Perfume, admin.site._registry)
