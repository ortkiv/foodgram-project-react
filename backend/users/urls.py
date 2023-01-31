from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyUserViewSet, SubscribeViewSet, SubscriptionsViewSet

router = DefaultRouter()

router.register('users', MyUserViewSet, basename='users')

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionsViewSet.as_view({'get': 'list'}),
        name='subscriptions'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        SubscribeViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='subscribe'
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
