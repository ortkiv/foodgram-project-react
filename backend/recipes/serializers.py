import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from ingredients.models import Ingredient
from rest_framework.serializers import (ImageField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField)
from rest_framework.validators import UniqueTogetherValidator
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

from .models import Favorite, IngredientInRecipe, InShopCart, Recipe

User = get_user_model()


class IngredientInRecipeSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient_id'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')

    def to_representation(self, instance):
        return {
            "id": instance.ingredient.id,
            "name": instance.ingredient.name,
            "measurement_unit": instance.ingredient.measurement_unit,
            "amount": instance.amount
        }


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(ModelSerializer):
    author = CustomUserSerializer(
        read_only=True
    )
    ingredients = IngredientInRecipeSerializer(
        many=True,
        source='ingredientinrecipe_set.all'
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated and Favorite.objects.filter(
            user=user,
            recipe=obj
        ).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated and InShopCart.objects.filter(
            user=user,
            recipe=obj
        ).exists():
            return True
        return False

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientinrecipe_set')['all']
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            if Ingredient.objects.filter(
                id=ingredient['ingredient_id'].id
            ).exists():
                IngredientInRecipe.objects.create(
                    recipe=recipe,
                    ingredient=ingredient['ingredient_id'],
                    amount=ingredient['amount']
                )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.tags.set(validated_data.get('tags', instance.tags))
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        ingredients = validated_data.get('ingredientinrecipe_set')['all']
        for ingredient in ingredients:
            current_ingredent = IngredientInRecipe.objects.filter(
                recipe=instance,
                ingredient=ingredient['ingredient_id']
            )
            if current_ingredent.exists():
                current_ingredent.update(
                    amount=ingredient['amount']
                )
            elif Ingredient.objects.filter(
                id=ingredient['ingredient_id'].id
            ).exists():
                IngredientInRecipe.objects.create(
                    recipe=instance,
                    ingredient=ingredient['ingredient_id'],
                    amount=ingredient['amount']
                )
        instance.save()
        return instance

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['tags'] = TagSerializer(instance.tags.all(), many=True).data
        repr['ingredients'] = IngredientInRecipeSerializer(
            IngredientInRecipe.objects.filter(recipe=instance).all(),
            many=True
        ).data
        return repr


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('recipe', 'user'),
                message="Один рецепт можно добавить"
                        "в избранное только один раз!"
            )
        ]

    def to_representation(self, instance):
        return {
            "id": instance.recipe.id,
            "name": instance.recipe.name,
            # "image": instance.recipe.image,
            "cooking_time": instance.recipe.cooking_time
        }


class InShopCartSerializer(ModelSerializer):
    class Meta:
        model = InShopCart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=InShopCart.objects.all(),
                fields=('recipe', 'user'),
                message="Один рецепт можно добавить"
                        "в список покупок только один раз!"
            )
        ]

    def to_representation(self, instance):
        return {
            "id": instance.recipe.id,
            "name": instance.recipe.name,
            # "image": instance.recipe.image,
            "cooking_time": instance.recipe.cooking_time
        }