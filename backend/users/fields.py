from rest_framework.serializers import ValidationError


class CurrentAuthorDefault:
    """Определяет атрибут author в FollowSerializer
    Запрещает подписываться на самого себя.
    """
    requires_context = True

    def __call__(self, serializer_field):
        request_user = serializer_field.parent.context.get('request').user
        author_id = serializer_field.context.get('view').kwargs.get('user_id')
        if request_user.id == author_id:
            raise ValidationError('Нельзя подписаться на самого себя!')
        return serializer_field.context.get('view').kwargs.get('user_id')
