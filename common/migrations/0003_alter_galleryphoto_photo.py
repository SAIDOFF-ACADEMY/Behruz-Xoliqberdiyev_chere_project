# Generated by Django 4.2 on 2024-07-03 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20240627_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryphoto',
            name='photo',
            field=models.ImageField(upload_to='photos/%Y/%m/'),
        ),
    ]
