# Generated by Django 2.2.4 on 2020-04-29 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('espumas', '0003_auto_20200429_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='densidad_objetivo_alta',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='densidad_objetivo_baja',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='densidad_tipo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='dureza_objetivo_alta',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='dureza_objetivo_baja',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='dureza_tipo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='flujo_de_aire_astm_alto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='flujo_de_aire_astm_bajo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='flujo_de_aire_astm_maximo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='flujo_de_aire_astm_minimo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='flujo_de_aire_campo_alto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='flujo_de_aire_campo_bajo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='flujo_de_aire_campo_maximo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='tipos_de_espuma',
            name='flujo_de_aire_campo_minimo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
