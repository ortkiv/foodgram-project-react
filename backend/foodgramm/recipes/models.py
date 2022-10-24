from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Ingridient(models.Model):
    title = models.CharField(
        'Название',
        max_length=200
    )
    quantity = models.IntegerField(
        'Колличество',
        validators=[MinValueValidator(0)]
    )
    measure_unit = models.CharField(
        'Единицы измерения',
        max_length=80
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Tag(models.Model):
    title = models.CharField(
        'Название',
        max_length=200
    )
    colour = models.CharField(
        'Цветовой HEX-код',
        max_length=200
    )
    slug = models.SlugField(
        'Slug',
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    title = models.CharField(
        'Название',
        max_length=200,
        help_text='Укажите название рецепта'
    )
    description = models.CharField(
        'Текстовое описание рецепта',
        max_length=500
    )
    # image = models.ImageField(
    #    'Катринка',
    #    upload_to='recipes/'
    # )
    # ingredients = models.ManyToManyField(
    #    Ingridient,
    #    through='RecipeIngridients',
    #    verbose_name='Ингридиенты',
    #    related_name='recipes'
    # )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
        related_name='recipes'
    )
    time = models.IntegerField(
        'Время приготовления в минутах',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'рецепты'


# class RecipeIngridients(models.Model):
#    recipe = models.ForeignKey(
#        Recipe,
#        on_delete=models.CASCADE
#    )
#    ingridients = models.ForeignKey(
#        Ingridient,
#        on_delete=models.CASCADE
#    )
