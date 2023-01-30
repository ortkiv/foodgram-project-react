from django.db import models

from colorfield.fields import ColorField


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200
    )
    color = ColorField(
        'Цвет',
        default='#FF0000'
    )
    slug = models.SlugField(
        'Slug',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name
