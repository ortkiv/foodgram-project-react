from rest_framework import mixins, viewsets


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
