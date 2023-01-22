from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Follow, IngredientInRecipe, Ingridient,
                            InShopCart, Recipe, Tag)
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import CustomPageNumberPagination
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, InShopCartSerializer,
                          RecipeSerializer, TagSerializer, UserSerializer,
                          UserWithRecipesSerializer)

User = get_user_model()


class IngridientViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingridient.objects.all()
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

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
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        obj = get_object_or_404(Favorite, recipe=recipe, user=user)
        obj.delete()
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
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        obj = get_object_or_404(InShopCart, recipe=recipe, user=user)
        obj.delete()
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


class MyUserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserSerializer


class SubscriptionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserWithRecipesSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(publisher__user=self.request.user)


class SubscribeViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination
    queryset = Follow.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            Follow,
            user=self.request.user,
            author=self.kwargs.get('user_id')
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.kwargs.get('user_id'))
        serializer.save(user=self.request.user, author=author)
