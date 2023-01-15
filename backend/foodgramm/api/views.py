from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsAuthor, IsReadOnly
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
    IngredientInRecipe,
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
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse

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
    permission_classes = (IsAuthor | IsReadOnly,)
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
        data = IngredientInRecipe.objects.filter(
            recipe__host_recipes__user=request.user
        ).values('ingredient', 'amount')
        data_ing = set(ing['ingredient'] for ing in data)
        data_clear = [
            {
                'ingredient': i,
                'amount': sum(
                    a['amount'] for a in data if a['ingredient'] == i
                )
            } for i in data_ing
        ]
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="file.pdf"'
        p = canvas.Canvas(response, pagesize=A4)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        p.setFont("FreeSans", 20)
        width = 200
        height = 770
        p.drawString(width, 800, 'Список покупок:')
        for x in data_clear:
            name = Ingridient.objects.get(id=x['ingredient']).name
            amount = x['amount']
            unit = Ingridient.objects.get(id=x['ingredient']).measurement_unit
            p.drawString(
                width,
                height,
                f'-  {name} - {amount}{unit}'
            )
            height -= 20
            if height <= 20:
                p.showPage()
                p.setFont("FreeSans", 20)
                height = 800
        p.showPage()
        p.save()
        return response


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
