# Generated by Django 2.2.4 on 2020-04-30 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrida', '0020_auto_20200430_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloqueproducido',
            name='alto_caliente',
            field=models.DecimalField(decimal_places=2, default=122, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='bloqueproducido',
            name='ancho_caliente',
            field=models.DecimalField(decimal_places=2, default=122, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='bloqueproducido',
            name='flujo_de_aire_caliente',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='bloqueproducido',
            name='largo_caliente',
            field=models.DecimalField(decimal_places=2, default=122, max_digits=10, null=True),
        ),
    ]
