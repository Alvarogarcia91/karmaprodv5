# Generated by Django 2.2.12 on 2020-07-02 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrida', '0025_auto_20200508_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloqueproducido',
            name='defecto',
            field=models.CharField(choices=[('sd', ''), ('ph', 'Pinhole'), ('g', 'Grieta'), ('v', 'Vena'), ('mm', 'Mal manejo'), ('fdm', 'Fuera de medida'), ('a', 'Algodonozo'), ('ma', 'Manchado')], default='sd', max_length=2),
        ),
    ]
