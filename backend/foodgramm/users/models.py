from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('auth_user', 'Auth_User'),
        ('admin', 'Admin'),
    )
    first_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email address'
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLE_CHOICES,
        default='guest',
        verbose_name='User role'
    )
