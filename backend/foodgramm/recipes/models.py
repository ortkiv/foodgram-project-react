from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from colorfield.fields import ColorField

User = get_user_model()


class Ingridient(models.Model):
    name = models.CharField(
        'Название',
        max_length=200
    )
    quantity = models.IntegerField(
        'Колличество',
        validators=[MinValueValidator(0)]
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=80
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self) -> str:
        return self.name


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
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    name = models.CharField(
        'Название',
        max_length=200,
        help_text='Укажите название рецепта'
    )
    text = models.TextField(
        'Текстовое описание рецепта',
        max_length=500
    )
    image = models.ImageField(
        'Катринка',
        upload_to='foodgramm/images/'
    )
    ingredients = models.ManyToManyField(
        Ingridient,
        verbose_name='Ингридиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэг'
    )
    cooking_time = models.IntegerField(
        'Время приготовления в минутах',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self) -> str:
        return self.name


# class RecipeTag(models.Model):
#    recipe = models.ForeignKey(
#        Recipe,
#        on_delete=models.CASCADE
#    )
#    tag = models.ForeignKey(
#        Tag,
#        on_delete=models.CASCADE
#    )


# class RecipeIngridients(models.Model):
#    recipe = models.ForeignKey(
#        Recipe,
#        on_delete=models.CASCADE
#    )
#    ingridients = models.ForeignKey(
#        Ingridient,
#        on_delete=models.CASCADE
#    )
