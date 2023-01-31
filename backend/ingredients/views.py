from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Ingredient
from .serializers import IngredientSerializer
from utils.filters import IngredientSearchFilter


class IngredientViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None
