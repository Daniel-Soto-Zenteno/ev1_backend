from io import StringIO
import tempfile

from django.core.files.base import ContentFile
from django.core.management import call_command
from django.test import TestCase, override_settings

from .models import Perfume


class CargarCatalogoTests(TestCase):
    def test_carga_repetible_con_fotos_sin_sobrescribir_precio_ni_inventario(self):
        with tempfile.TemporaryDirectory() as media, override_settings(MEDIA_ROOT=media):
            call_command('cargar_catalogo', stdout=StringIO())
            self.assertEqual(Perfume.objects.count(), 8)
            self.assertFalse(Perfume.objects.filter(en_stock=True).exists())
            self.assertTrue(all(p.imagen.storage.exists(p.imagen.name) for p in Perfume.objects.all()))
            perfume = Perfume.objects.get(nombre='French Avenue Liquid Brun EDP')
            perfume.precio = 41000
            perfume.en_stock = True
            perfume.save()
            original_image = perfume.imagen.name
            call_command('cargar_catalogo', stdout=StringIO())
            perfume.refresh_from_db()
            self.assertEqual(Perfume.objects.count(), 8)
            self.assertEqual(perfume.precio, 41000)
            self.assertTrue(perfume.en_stock)
            self.assertEqual(perfume.imagen.name, original_image)

    def test_repone_foto_ausente_y_conserva_foto_personalizada(self):
        with tempfile.TemporaryDirectory() as media, override_settings(MEDIA_ROOT=media):
            call_command('cargar_catalogo', stdout=StringIO())
            perfume = Perfume.objects.get(nombre='Halloween Man X')
            perfume.imagen.storage.delete(perfume.imagen.name)
            call_command('cargar_catalogo', stdout=StringIO())
            perfume.refresh_from_db()
            self.assertTrue(perfume.imagen.storage.exists(perfume.imagen.name))
            perfume.imagen.save('foto-personalizada.jpg', ContentFile(b'foto-propia'), save=True)
            custom_name = perfume.imagen.name
            call_command('cargar_catalogo', stdout=StringIO())
            perfume.refresh_from_db()
            self.assertEqual(perfume.imagen.name, custom_name)
            with perfume.imagen.open('rb') as image:
                self.assertEqual(image.read(), b'foto-propia')
