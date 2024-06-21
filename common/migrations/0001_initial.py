# Generated by Django 4.2 on 2024-06-21 10:20

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('title_ru', models.CharField(max_length=250, null=True)),
                ('title_uz', models.CharField(max_length=250, null=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('content_ru', ckeditor_uploader.fields.RichTextUploadingField(null=True)),
                ('content_uz', ckeditor_uploader.fields.RichTextUploadingField(null=True)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contact_telegram', models.CharField(max_length=120)),
                ('contact_phone', models.CharField(max_length=30)),
                ('longitude', models.BigIntegerField()),
                ('latitude', models.BigIntegerField()),
                ('location_text', models.TextField()),
                ('location_text_ru', models.TextField(null=True)),
                ('location_text_uz', models.TextField(null=True)),
                ('working_hours_start', models.TimeField()),
                ('working_hours_end', models.TimeField()),
                ('telegram_bot', models.CharField(max_length=120)),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]
