# Generated by Django 2.2 on 2020-12-16 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20201215_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='title',
            field=models.CharField(max_length=70, unique=True),
        ),
    ]
