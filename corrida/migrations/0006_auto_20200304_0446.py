# Generated by Django 2.2.4 on 2020-03-04 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrida', '0005_auto_20200304_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corrida',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
