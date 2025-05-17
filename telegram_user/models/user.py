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

    restaurant = models.ManyToManyField(
        "ActiveRestaurant",
        blank=True,
        related_name="users",
    )

    does_want_notifications = models.BooleanField(
        default=True,
    )

    def change_status(self):
        self.does_want_notifications = not self.does_want_notifications
        self.save()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"