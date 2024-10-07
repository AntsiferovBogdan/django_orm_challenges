from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Laptop(models.Model):
    class Meta:
        get_latest_by = 'created_at'
        index_together = ['brand', 'price']
        ordering = ['price']
        verbose_name = 'laptop'
        verbose_name_plural = 'laptops'

    BRAND_CHOICES = [
        ('LG', 'LG'),
        ('Samsung', 'Samsung'),
        ('Apple', 'Apple'),
    ]

    brand = models.CharField(max_length=16, choices=BRAND_CHOICES)
    release_year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1979),
            MaxValueValidator(datetime.now().year + 1),
        ]
    )
    ram = models.PositiveSmallIntegerField()
    storage = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        data = {
            'brand': self.brand,
            'release_year': self.release_year,
            'ram': self.ram,
            'storage': self.storage,
            'price': self.price,
            'stock': self.stock,
            'created_at': self.created_at.isoformat(),
        }
        return data

    def __str__(self):
        return (
            f'{self.brand}, {self.release_year} года, {self.ram}GB, {self.storage}GB. '
            f'Цена: {self.price}. Кол-во на складе: {self.stock}. Добавлен {self.created_at}'
        )


class Post(models.Model):
    class Meta:
        get_latest_by = 'published_at'
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    STATUS_CHOICES = [
        ('published', 'published'),
        ('not published', 'not published'),
        ('banned', 'banned'),
    ]

    CATEGORY_CHOICES = [
        (None, 'No category'),
        ('it', 'IT'),
        ('hobby', 'Hobby'),
        ('videogames', 'Videogames'),
    ]

    title = models.CharField(max_length=128)
    author = models.CharField(max_length=64)
    text = models.CharField(max_length=16384)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    created_at = models.DateField(auto_now_add=True)
    published_at = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'published' and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def to_json(self):
        data = {
            'title': self.title,
            'author': self.author,
            'text': self.text,
            'status': self.status,
            'created_at': self.created_at.isoformat(),  # Преобразуем дату в ISO формат
            'published_at': self.published_at.isoformat() if self.published_at else None,  # Преобразуем дату в ISO формат
            'category': self.category,
        }
        return data

    def __str__(self):
        return (
            f'{self.title} by {self.author}. Status: {self.status}'
            f'{self.category}'
            f'published at {self.published_at}, create_at {self.created_at}'
        )
