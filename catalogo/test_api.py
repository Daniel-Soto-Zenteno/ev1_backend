from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from .models import Perfume


class PerfumeApiTests(APITestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(
            username='admin_api', password='solo-para-pruebas', is_staff=True,
        )
        self.reader = get_user_model().objects.create_user(
            username='lector_api', password='solo-para-pruebas',
        )
        self.perfume = Perfume.objects.create(
            nombre='Dulce Noche', categoria='Femenino', precio=15000, ml=100,
        )
        self.data = {
            'nombre': 'Citrus Fresh', 'categoria': 'Unisex', 'precio': '12000',
            'ml': 50, 'en_stock': True, 'destacado': False,
        }
        self.list_url = reverse('api-perfume-list')
        self.detail_url = reverse('api-perfume-detail', args=[self.perfume.pk])

    def authenticate(self, user=None):
        user = user or self.staff
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': user.username, 'password': 'solo-para-pruebas',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        return response.data

    def test_list_and_detail_require_jwt(self):
        for url in (self.list_url, self.detail_url):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 401)
            self.assertIn('detail', response.json())
        self.authenticate(self.reader)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.json()[0]['id'], self.perfume.pk)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nombre'], 'Dulce Noche')

    def test_create_persists_and_is_visible_on_website(self):
        self.authenticate()
        response = self.client.post(self.list_url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
        created = Perfume.objects.get(pk=response.data['id'])
        self.assertEqual(created.precio, Decimal('12000'))
        self.assertContains(self.client.get(reverse('lista_perfumes')), 'Citrus Fresh')
        self.assertIn('creado', response.json())

    def test_put_and_patch_persist(self):
        self.authenticate()
        response = self.client.put(self.detail_url, self.data, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.client.patch(self.detail_url, {'precio': '18000'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.perfume.refresh_from_db()
        self.assertEqual(self.perfume.nombre, 'Citrus Fresh')
        self.assertEqual(self.perfume.precio, Decimal('18000'))
        self.assertEqual(self.perfume.ml, 50)

    def test_delete_persists(self):
        self.authenticate()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Perfume.objects.filter(pk=self.perfume.pk).exists())

    def test_invalid_data_returns_json_and_does_not_save(self):
        self.authenticate()
        cases = [({}, 'nombre'), ({'nombre': ''}, 'nombre'),
                 ({'nombre': '  '}, 'nombre'), ({'nombre': 'ab'}, 'nombre'),
                 ({'precio': 0}, 'precio'), ({'precio': -1}, 'precio'),
                 ({'precio': 'texto'}, 'precio'), ({'ml': 0}, 'ml'),
                 ({'ml': 'texto'}, 'ml'), ({'categoria': 'Otra'}, 'categoria'),
                 ({'destacado': True, 'en_stock': False}, 'destacado')]
        for changes, field in cases:
            with self.subTest(changes=changes):
                payload = {} if not changes else self.data | changes
                response = self.client.post(self.list_url, payload, format='json')
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.json())
                self.assertEqual(Perfume.objects.count(), 1)

    def test_patch_validates_existing_state_without_mutating_on_failure(self):
        self.perfume.destacado = True
        self.perfume.save()
        self.authenticate()
        response = self.client.patch(self.detail_url, {'en_stock': False}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('destacado', response.json())
        self.perfume.refresh_from_db()
        self.assertTrue(self.perfume.en_stock)

    def test_missing_token_blocks_every_write(self):
        for method, url, data in [
            ('post', self.list_url, self.data), ('put', self.detail_url, self.data),
            ('patch', self.detail_url, {'precio': 25000}), ('delete', self.detail_url, {}),
        ]:
            with self.subTest(method=method):
                response = getattr(self.client, method)(url, data, format='json')
                self.assertEqual(response.status_code, 401)
                self.assertIn('detail', response.json())
        self.assertEqual(Perfume.objects.count(), 1)
        self.perfume.refresh_from_db()
        self.assertEqual(self.perfume.precio, 15000)

    def test_non_staff_token_blocks_every_write(self):
        self.authenticate(self.reader)
        for method, url, data in [
            ('post', self.list_url, self.data), ('put', self.detail_url, self.data),
            ('patch', self.detail_url, {'precio': 25000}), ('delete', self.detail_url, {}),
        ]:
            with self.subTest(method=method):
                response = getattr(self.client, method)(url, data, format='json')
                self.assertEqual(response.status_code, 403)
                self.assertIn('detail', response.json())
        self.assertEqual(Perfume.objects.count(), 1)
        self.perfume.refresh_from_db()
        self.assertEqual(self.perfume.precio, 15000)

    def test_invalid_expired_and_inactive_tokens_are_rejected(self):
        expired = AccessToken.for_user(self.staff)
        expired.set_exp(lifetime=timedelta(seconds=-1))
        for token in ('invalido', str(expired)):
            with self.subTest(token_kind='expired' if token != 'invalido' else 'invalid'):
                self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
                self.assertEqual(self.client.post(self.list_url, self.data, format='json').status_code, 401)
        token = AccessToken.for_user(self.staff)
        self.staff.is_active = False
        self.staff.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))
        self.assertEqual(self.client.post(self.list_url, self.data, format='json').status_code, 401)
        self.assertEqual(Perfume.objects.count(), 1)

    def test_unknown_id_returns_json_404(self):
        self.authenticate()
        url = reverse('api-perfume-detail', args=[999999])
        for method in ('get', 'put', 'patch', 'delete'):
            with self.subTest(method=method):
                response = getattr(self.client, method)(url, self.data, format='json')
                self.assertEqual(response.status_code, 404)
                self.assertIn('detail', response.json())

    def test_read_only_fields_and_normalized_name(self):
        self.authenticate()
        response = self.client.post(self.list_url, self.data | {
            'nombre': '  Citrus Fresh  ', 'id': 999999, 'creado': '2000-01-01T00:00:00Z',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data['id'], 999999)
        self.assertEqual(response.data['nombre'], 'Citrus Fresh')
        self.assertFalse(response.data['creado'].startswith('2000-01-01'))

    def test_malformed_json_returns_400(self):
        self.authenticate()
        response = self.client.post(self.list_url, '{', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.json())

    def test_session_login_does_not_replace_jwt(self):
        client = APIClient()
        client.force_login(self.staff)
        self.assertEqual(client.post(self.list_url, self.data, format='json').status_code, 401)
