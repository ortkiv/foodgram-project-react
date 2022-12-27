from rest_framework.viewsets import ModelViewSet
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserWithRecipesSerializer,
    FollowSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingridient, Tag, Recipe
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


class IngridientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingridient.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = None


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'author',
        'tags'
    )
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer


class SubscriptionsViewSet(ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = UserWithRecipesSerializer

    def get_queryset(self):
        return User.objects.filter(publisher__user=self.request.user)


class SubscribeViewSet(ModelViewSet):
    pagination_class = None
    serializer_class = FollowSerializer

    def get_queryset(self):
        return User.objects.filter(publisher__user=self.request.user)

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.kwargs.get('user_id'))
        serializer.save(user=self.request.user, author=author)
