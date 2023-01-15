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
        max_length=200,
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
        upload_to='foodgramm/images/',
        blank=True
    )
    ingredients = models.ManyToManyField(
        Ingridient,
        through='IngredientInRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэг',
        blank=True
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


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique IngredientInRecipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='publisher',
        verbose_name='Автор подписки'
    )

    class Meta:
        verbose_name = 'Подписку'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique follow'
            )
        ]

    def __str__(self) -> str:
        return f'{self.author} - {self.user}'


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
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
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
