# Generated by Django 2.2.12 on 2020-07-02 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('espumas', '0010_remove_bloquemedidas_medida_dispobible'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloquemedidas',
            name='familia_de_medidas',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
