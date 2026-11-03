from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase


class JwtTests(APITestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username='usuario_prueba_jwt', password='solo-para-pruebas'
        )

    def test_obtener_y_renovar_tokens(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'usuario_prueba_jwt', 'password': 'solo-para-pruebas'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        renovacion = self.client.post(reverse('token_refresh'), {
            'refresh': response.data['refresh']
        }, format='json')
        self.assertEqual(renovacion.status_code, 200)
        self.assertIn('access', renovacion.data)

    def test_password_incorrecta(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'usuario_prueba_jwt', 'password': 'incorrecta'
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_refresh_invalido(self):
        response = self.client.post(reverse('token_refresh'), {'refresh': 'invalido'}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_usuario_inactivo(self):
        self.usuario.is_active = False
        self.usuario.save()
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'usuario_prueba_jwt', 'password': 'solo-para-pruebas'
        }, format='json')
        self.assertEqual(response.status_code, 401)
