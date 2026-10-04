from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('catalogo', '0001_initial')]
    operations = [
        migrations.AddField(
            model_name='perfume',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='perfumes/', verbose_name='imagen'),
        ),
    ]
