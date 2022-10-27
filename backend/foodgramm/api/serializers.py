from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField
)
from djoser.serializers import UserSerializer, UserCreateSerializer
from users.models import User
from recipes.models import Ingridient, Tag, Recipe


class UserSerializer(UserSerializer):
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


class UserCreateSerializer(UserCreateSerializer):
    class Meta():
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingridient
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    tags = SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = '__all__'
