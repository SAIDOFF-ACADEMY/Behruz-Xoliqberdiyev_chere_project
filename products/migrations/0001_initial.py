# Generated by Django 4.2 on 2024-06-27 06:30

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('name_ru', models.CharField(max_length=100, null=True, verbose_name='name')),
                ('name_uz', models.CharField(max_length=100, null=True, verbose_name='name')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='content')),
                ('content_ru', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='content')),
                ('content_uz', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='content')),
                ('price', models.BigIntegerField()),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='FreeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('count', models.IntegerField()),
                ('free_count', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='free_products', to='products.product')),
            ],
            options={
                'verbose_name': 'Free Product',
                'verbose_name_plural': 'Free Products',
                'db_table': 'free_products',
            },
        ),
    ]
