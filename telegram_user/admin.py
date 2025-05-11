from django.contrib import admin

from telegram_user.models import ActiveRestaurant, AvailableRestaurant
# Register your models here.

from telegram_user.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "telegram_id",
        "telegram_username",
    ]
    search_fields = ["telegram_id", "telegram_username"]
    list_filter = ["telegram_id", "telegram_username"]
    list_per_page = 20
    readonly_fields = ["last_login", "date_joined", "telegram_id"]
    ordering = ["date_joined", "last_login"]

    class Meta:
        model = User
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"


@admin.register(ActiveRestaurant)
class ActiveRestaurantAdmin(admin.ModelAdmin):
    list_display = [
        "restaurant",
    ]
    search_fields = ["restaurant"]
    list_filter = ["restaurant"]
    list_per_page = 20
    ordering = ["restaurant"]

    class Meta:
        model = ActiveRestaurant
        verbose_name = "Active Restaurant"
        verbose_name_plural = "Active Restaurants"

@admin.register(AvailableRestaurant)
class AvailableRestaurantAdmin(admin.ModelAdmin):
    list_display = [
        "restaurant_code",
        "restaurant_name",
    ]
    search_fields = ["restaurant_code", "restaurant_name"]
    list_filter = ["restaurant_code", "restaurant_name"]
    list_per_page = 20
    ordering = ["restaurant_code", "restaurant_name"]

    class Meta:
        model = AvailableRestaurant
        verbose_name = "Available Restaurant"
        verbose_name_plural = "Available Restaurants"