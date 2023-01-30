from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


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
        Ingredient,
        through='IngredientInRecipe'
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
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self) -> str:
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique IngredientInRecipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='Владелец_избранного'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='fav_recipes',
        verbose_name='рецепт_из_избранного'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique favorite'
            )
        ]

    def __str__(self) -> str:
        return f'{self.recipe} - {self.user}'


class InShopCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='host',
        verbose_name='Владелец_списка'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='host_recipes',
        verbose_name='рецепт_из_списка'
    )

    class Meta:
        verbose_name = 'рецепт_из_списка_покупок'
        verbose_name_plural = 'рецепты_из_списка_покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique inshopcard'
            )
        ]

    def __str__(self) -> str:
        return f'{self.recipe} - {self.user}'
