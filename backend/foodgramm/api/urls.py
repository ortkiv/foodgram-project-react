from django.urls import include, path
from .views import (
    IngridientViewSet,
    TagViewSet,
    RecipeViewSet,
    # SubscriptionsViewSet,
    # SubscribeViewSet,
    UserViewSet
)
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('ingredients', IngridientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
# router.register(
#    'users/subscriptions',
#    SubscriptionsViewSet,
#    basename='subscriptions'
# )
# router.register(
#    r'users/(?P<user_id>\d+)/subscribe',
#    SubscribeViewSet,
# )
# )


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
