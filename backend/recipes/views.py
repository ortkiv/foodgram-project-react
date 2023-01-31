from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Favorite, IngredientInRecipe, InShopCart, Recipe
from .serializers import (FavoriteSerializer, InShopCartSerializer,
                          RecipeSerializer)
from ingredients.models import Ingredient
from utils.filters import RecipeFilter
from utils.pagination import CustomPageNumberPagination

User = get_user_model()


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def static_post(request, pk, serializer):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        data = {
            'recipe': recipe.id,
            'user': user.id
        }
        serializer = serializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def static_delete(request, pk, model):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        obj = get_object_or_404(model, recipe=recipe, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return self.static_post(
            request=request,
            pk=pk,
            serializer=FavoriteSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        return self.static_delete(request=request, pk=pk, model=Favorite)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        return self.static_post(
            request=request,
            pk=pk,
            serializer=InShopCartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        return self.static_delete(request=request, pk=pk, model=InShopCart)

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
            name = Ingredient.objects.get(id=x['ingredient']).name
            amount = x['amount']
            unit = Ingredient.objects.get(id=x['ingredient']).measurement_unit
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
