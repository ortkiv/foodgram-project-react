from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from ingredients.views import IngredientViewSet
from recipes.views import RecipeViewSet
from rest_framework.routers import DefaultRouter
from tags.views import TagViewSet
from users.views import MyUserViewSet, SubscribeViewSet, SubscriptionsViewSet

router = DefaultRouter()

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('users', MyUserViewSet, basename='users')

urlpatterns = [
    path(
        'api/users/subscriptions/',
        SubscriptionsViewSet.as_view({'get': 'list'}),
        name='subscriptions'
    ),
    path(
        'api/users/<int:user_id>/subscribe/',
        SubscribeViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='subscribe'
    ),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
]
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
