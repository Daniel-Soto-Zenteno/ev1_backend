from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Perfume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('categoria', models.CharField(choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino'), ('Unisex', 'Unisex')], max_length=10, verbose_name='categoría')),
                ('precio', models.DecimalField(decimal_places=0, max_digits=10, validators=[MinValueValidator(1)])),
                ('ml', models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='formato en ml')),
                ('en_stock', models.BooleanField(default=True, verbose_name='disponible')),
                ('destacado', models.BooleanField(default=False)),
                ('creado', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['nombre', 'pk']},
        ),
    ]
