import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import (Favorite, Follow, IngredientInRecipe, Ingridient,
                            InShopCart, Recipe, Tag)
from rest_framework.serializers import (CurrentUserDefault, ImageField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField,
                                        StringRelatedField, ValidationError)
from rest_framework.validators import UniqueTogetherValidator

from .fields import CurrentAuthorDefault

User = get_user_model()


class UserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta():
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated and Follow.objects.filter(
            user=user,
            author=obj
        ).exists():
            return True
        return False


class UserCreateSerializer(UserCreateSerializer):
    class Meta():
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingridient
        fields = '__all__'


class IngredientInRecipeSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(
        queryset=Ingridient.objects.all(),
        source='ingredient_id'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')
        # validators = [
        #    UniqueTogetherValidator(
        #        queryset=IngredientInRecipe.objects.all(),
        #        fields=('id', 'amount'),
        #        message="Ингредиент уже есть в рецепте! "
        #    )
        # ]

    def to_representation(self, instance):
        return {
            "id": instance.ingredient.id,
            "name": instance.ingredient.name,
            "measurement_unit": instance.ingredient.measurement_unit,
            "amount": instance.amount
        }


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(ModelSerializer):
    author = UserSerializer(
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
            if Ingridient.objects.filter(
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
            elif Ingridient.objects.filter(
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


class RecipeMinifiedSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserWithRecipesSerializer(UserSerializer):
    recipes = RecipeMinifiedSerializer(
        many=True
    )
    is_subscribed = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated and Follow.objects.filter(
            user=user,
            author=obj
        ).exists():
            return True
        return False


class FollowSerializer(ModelSerializer):
    user = StringRelatedField(
        default=CurrentUserDefault()
    )
    author = StringRelatedField(
        default=CurrentAuthorDefault()
    )

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('author', 'user'),
                message="На одного пользователя "
                        "можно подписаться только один раз!"
            )
        ]

    def validate(self, data):
        if self.context.get('request').user == data.get('author'):
            raise ValidationError(
                "Нельзя подписаться на самого себя!"
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        repr = UserWithRecipesSerializer(
            instance.author,
            context={"request": request}
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
