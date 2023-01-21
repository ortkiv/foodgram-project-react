from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email address'
    )
    is_subscribed = models.BooleanField(
        default=False
    )
