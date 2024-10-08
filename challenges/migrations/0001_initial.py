# Generated by Django 4.2.3 on 2024-09-26 10:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('author_full_name', models.CharField(max_length=256)),
                ('isbn', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('author', models.CharField(max_length=64)),
                ('text', models.CharField(max_length=16384)),
                ('status', models.CharField(choices=[('published', 'published'), ('not published', 'not published'), ('banned', 'banned')], max_length=16)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('published_at', models.DateField(blank=True, null=True)),
                ('category', models.CharField(choices=[('IT', 'IT'), ('Hobby', 'Hobby'), ('Videogames', 'Videogames')], max_length=32)),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ['-created_at'],
                'get_latest_by': 'published_at',
            },
        ),
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(choices=[('LG', 'LG'), ('Samsung', 'Samsung'), ('Apple', 'Apple')], max_length=16)),
                ('release_year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1979), django.core.validators.MaxValueValidator(2025)])),
                ('ram', models.PositiveSmallIntegerField()),
                ('storage', models.PositiveSmallIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('stock', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'laptop',
                'verbose_name_plural': 'laptops',
                'ordering': ['price'],
                'get_latest_by': 'created_at',
                'index_together': {('brand', 'price')},
            },
        ),
    ]
