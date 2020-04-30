# Generated by Django 2.2.4 on 2020-04-29 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrida', '0017_remove_bloqueproducido_lote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('no_de_lote', models.CharField(max_length=100)),
                ('dureza_capturada', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sag_factor_capturado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('densidad_capturada', models.DecimalField(decimal_places=2, max_digits=10)),
                ('flujo_de_aire_astm_capturado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pruebas_realizadas', models.BooleanField(default=False)),
                ('pruebas_pasadas', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Lote',
            },
        ),
    ]
