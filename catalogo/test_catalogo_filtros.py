from django.test import TestCase
from django.urls import reverse
from .models import Perfume


class CatalogoFiltrosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Perfume.objects.create(nombre='Citrus Fresh', categoria='Unisex', precio=12000, ml=50)
        Perfume.objects.create(nombre='Citrus Noche', categoria='Masculino', precio=19000, ml=100, en_stock=False)
        Perfume.objects.create(nombre='Rosa', categoria='Femenino', precio=15000, ml=100)

    def test_busqueda_categoria_y_stock_se_combinan(self):
        response = self.client.get(reverse('lista_perfumes'), {'q': 'CITRUS', 'categoria': 'Unisex', 'disponible': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['perfumes'].values_list('nombre', flat=True)), ['Citrus Fresh'])
        self.assertEqual(response.context['total_productos'], 1)

    def test_orden_por_precio_y_entrada_no_permitida(self):
        response = self.client.get(reverse('lista_perfumes'), {'orden': 'precio_desc'})
        self.assertEqual(list(response.context['perfumes'].values_list('precio', flat=True)), [19000, 15000, 12000])
        response = self.client.get(reverse('lista_perfumes'), {'orden': 'no_existe', 'categoria': 'Otra'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['orden_actual'], 'nombre')
        self.assertEqual(response.context['total_productos'], 3)

    def test_estado_vacio_y_formato_precio(self):
        self.assertContains(self.client.get(reverse('lista_perfumes')), '$12.000')
        response = self.client.get(reverse('lista_perfumes'), {'q': 'inexistente'})
        self.assertContains(response, 'Sin coincidencias')
        self.assertEqual(response.context['total_productos'], 0)
