from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .serializers import (
    IngredientSerializer,
    InShopCartSerializer,
    TagSerializer,
    RecipeSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserWithRecipesSerializer,
    FavoriteSerializer,
    FollowSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (
    Ingridient,
    InShopCart,
    Favorite,
    Follow,
    Tag,
    Recipe
)
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if request.method == 'POST':
            data = {
                'recipe': recipe.id,
                'user': user.id
            }
            ser = FavoriteSerializer(data=data, context={'request': request})
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        favorite = get_object_or_404(Favorite, recipe=recipe, user=user)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if request.method == 'POST':
            data = {
                'recipe': recipe.id,
                'user': user.id
            }
            ser = InShopCartSerializer(data=data, context={'request': request})
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        favorite = get_object_or_404(InShopCart, recipe=recipe, user=user)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        serializer = UserSerializer(
            request.user,
            context={'request': request}
        )
        return Response(serializer.data)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False)
    def me(self, request, pk=None):
        serializer = UserSerializer(
            request.user,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=False, permission_classes=[IsOwner])
    def subscriptions(self, request):
        users = User.objects.filter(publisher__user=request.user)
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserWithRecipesSerializer(
                page,
                context={'request': request},
                many=True
            )
            return self.get_paginated_response(serializer.data)
        serializer = UserWithRecipesSerializer(
            users,
            context={'request': request},
            many=True
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, id=pk)
        user = request.user
        if request.method == 'POST':
            data = {
                'author': author.id,
                'user': user.id
            }
            ser = FollowSerializer(data=data, context={'request': request})
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        follow = get_object_or_404(Follow, author=author, user=user)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class SubscriptionsViewSet(mixins.ListModelMixin, GenericViewSet):
#    pagination_class = PageNumberPagination
#    serializer_class = UserWithRecipesSerializer

#    def get_queryset(self):
#        return User.objects.filter(publisher__user=self.request.user)


# class SubscribeViewSet(
#    mixins.CreateModelMixin,
#    mixins.DestroyModelMixin,
#    GenericViewSet
# ):
#    pagination_class = None
#    serializer_class = FollowSerializer

#    def get_queryset(self):
#        return Follow.objects.filter(user=self.request.user)

#    def perform_create(self, serializer):
#        author = get_object_or_404(User, id=self.kwargs.get('user_id'))
#        serializer.save(user=self.request.user, author=author)
