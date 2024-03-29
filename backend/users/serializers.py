from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjoserUserCreate
from djoser.serializers import UserSerializer as DjoserUser
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        ValidationError)
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow
from recipes.models import Recipe

User = get_user_model()


class CustomUserSerializer(DjoserUser):
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


class CustomUserCreateSerializer(DjoserUserCreate):
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


class RecipeMinifiedSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserWithRecipesSerializer(CustomUserSerializer):
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
        if self.context.get('request').user.id == data.get('author').id:
            raise ValidationError('Нельзя подписаться на самого себя!')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return UserWithRecipesSerializer(
            instance.author,
            context={"request": request}
        ).data
