from django.contrib.auth import get_user_model
from rest_framework.serializers import (ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField, ValidationError)
from rest_framework.validators import UniqueTogetherValidator

from .fields import Base64ImageField
from .models import Favorite, IngredientInRecipe, InShopCart, Recipe
from ingredients.models import Ingredient
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

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
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    @staticmethod
    def calculate_field_value(self, obj, model):
        user = self.context.get('request').user
        if user.is_authenticated and model.objects.filter(
            user=user,
            recipe=obj
        ).exists():
            return True
        return False

    @staticmethod
    def create_ingred_in_recipe(ingredients, recipe):
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['ingredient_id'],
                amount=ingredient['amount']
            )

    def get_is_favorited(self, obj):
        return self.calculate_field_value(
            self=self,
            obj=obj,
            model=Favorite
        )

    def get_is_in_shopping_cart(self, obj):
        return self.calculate_field_value(
            self=self,
            obj=obj,
            model=InShopCart
        )

    def validate(self, data):
        ingredients = data['ingredientinrecipe_set']['all']
        ids = []
        for ingredient in ingredients:
            if ingredient['ingredient_id'] in ids:
                raise ValidationError('Задвоенный ингредиент в рецепте!')
            ids.append(ingredient['ingredient_id'])
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientinrecipe_set')['all']
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingred_in_recipe(
            ingredients=ingredients,
            recipe=recipe
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
        self.create_ingred_in_recipe(
            ingredients=ingredients,
            recipe=instance
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
