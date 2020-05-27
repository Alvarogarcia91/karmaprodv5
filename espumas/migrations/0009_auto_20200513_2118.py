# Generated by Django 2.2.4 on 2020-05-13 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('espumas', '0008_auto_20200513_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='flujo_de_aire_astm_objetivo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='flujo_de_aire_campo_objetivo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]