from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from utils.pagination import CustomPageNumberPagination
from rest_framework import mixins, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .models import Follow
from .serializers import (CustomUserSerializer, FollowSerializer,
                          UserWithRecipesSerializer)

User = get_user_model()


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class ListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class MyUserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CustomUserSerializer


class SubscriptionsViewSet(ListViewSet):
    serializer_class = UserWithRecipesSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(publisher__user=self.request.user)


class SubscribeViewSet(CreateDestroyViewSet):
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
