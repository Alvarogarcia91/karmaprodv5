# Generated by Django 2.2.12 on 2020-09-02 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrida', '0029_corrida_fecha_produccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloqueproducido',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
    ]
