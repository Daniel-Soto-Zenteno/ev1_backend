import json
from decimal import Decimal
from pathlib import Path

from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalogo.models import Perfume


class Command(BaseCommand):
    help = 'Carga las fragancias iniciales y repone sus fotografías sin sobrescribir datos existentes.'

    def handle(self, *args, **options):
        source = Path(__file__).resolve().parents[2] / 'data' / 'catalogo.json'
        records = json.loads(source.read_text(encoding='utf-8'))
        assets = []
        for record in records:
            image_path = finders.find('catalogo/images/perfumes/' + record['imagen'])
            if not image_path:
                raise CommandError('Falta la fotografía: ' + record['imagen'])
            assets.append(Path(image_path))

        created_count = 0
        image_count = 0
        with transaction.atomic():
            for record, image_path in zip(records, assets):
                perfume, created = Perfume.objects.get_or_create(
                    nombre=record['nombre'], ml=record['ml'],
                    defaults={
                        'categoria': record['categoria'],
                        'precio': Decimal(record['precio']),
                        'en_stock': False,
                        'destacado': False,
                    },
                )
                if created:
                    perfume.full_clean()
                    created_count += 1
                if perfume.imagen and perfume.imagen.storage.exists(perfume.imagen.name):
                    continue
                with image_path.open('rb') as content:
                    perfume.imagen.save(record['imagen'], File(content), save=True)
                image_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Catálogo listo: {created_count} productos creados y {image_count} imágenes cargadas.'
        ))
