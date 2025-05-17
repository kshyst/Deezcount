import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_base.settings")
django.setup()

from asgiref.sync import sync_to_async
from telegram import (
    Update,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from telegram_user.models import ActiveRestaurant, User
from telegram_bot.statics.menu_ranges import DELETE_RESTAURANT
from telegram_bot.statics.reply_keyboards import main_menu_buttons, in_menu_buttons


async def show_active_restaurants_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    restaurants = []
    telegram_user = await sync_to_async(User.objects.get)(telegram_id=update.effective_user.id)
    restaurants_data = await sync_to_async(list)(
        ActiveRestaurant.objects.filter(users=telegram_user)
        .select_related("restaurant")
        .values_list("restaurant__restaurant_name", "id")
    )

    for name, restaurant_id in restaurants_data:
        restaurants.append((name, restaurant_id))

    context.user_data['restaurants'] = restaurants

    message = "لیست رستوران های فعال شما به شرح زیر است. برای حذف کردن رستوران مورد نظر شماره آن را وارد کنید.\n\n"
    num = 1

    if len(restaurants) > 0:
        for restaurant in restaurants:
            message += f"{num}. {restaurant[0]}\n"
            num += 1


    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_to_message_id=update.effective_message.id,
        reply_markup=ReplyKeyboardMarkup(
            in_menu_buttons, one_time_keyboard=True
        ),
    )

    return DELETE_RESTAURANT

async def delete_restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_restaurant = update.message.text

    try:
        selected_restaurant = int(selected_restaurant)
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="شماره وارد کنید."
        )
        return DELETE_RESTAURANT

    if selected_restaurant > len(context.user_data['restaurants']) or selected_restaurant <= 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="شماره رستوران مورد نظر وجود ندارد."
        )
        return DELETE_RESTAURANT

    restaurant = context.user_data['restaurants'][selected_restaurant - 1]

    user = await sync_to_async(User.objects.get)(telegram_id=update.effective_user.id)
    restaurant_obj = await sync_to_async(ActiveRestaurant.objects.get)(id=restaurant[1])
    await sync_to_async(user.restaurant.remove)(restaurant_obj)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="رستوران مورد نظر با موفقیت حذف شد.",
        reply_markup=ReplyKeyboardMarkup(
            main_menu_buttons, one_time_keyboard=True
        )
    )

    return ConversationHandler.END