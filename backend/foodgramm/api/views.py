from rest_framework.viewsets import ModelViewSet
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeSerializer,
    UserSerializer,
    UserCreateSerializer
)
from recipes.models import Ingridient, Tag, Recipe, User
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters


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
    pagination_class = PageNumberPagination


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
