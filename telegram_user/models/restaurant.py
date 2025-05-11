from django.db import models


class AvailableRestaurant(models.Model):

    restaurant_code = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        blank=False,
    )

    restaurant_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.restaurant_name

    class Meta:
        ordering = ['restaurant_name']
        verbose_name = 'Available Restaurant'
        verbose_name_plural = 'Available Restaurants'


class ActiveRestaurant(models.Model):
    restaurant = models.OneToOneField(
        AvailableRestaurant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.restaurant.restaurant_name

    class Meta:
        ordering = ['restaurant']
        verbose_name = 'Active Restaurant'
        verbose_name_plural = 'Active Restaurants'