from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = [
        "password",
    ]

    telegram_id = models.BigIntegerField(
        primary_key=True,
        unique=True,
        null=False,
        blank=False,
        default=0,
    )

    telegram_username = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        default="",
    )

    telegram_account_name = models.CharField(
        max_length=255,
    )

    restaurant = models.ForeignKey(
        "ActiveRestaurant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    does_want_notifications = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"