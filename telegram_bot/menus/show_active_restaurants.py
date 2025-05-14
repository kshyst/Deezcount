from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from telegram_user.models import User


async def show_active_restaurants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.effective_user.id)
    user = await sync_to_async(User.objects.get)(telegram_id=user_id)

    if not user:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="شما در سیستم ثبت نام نشده اید. لطفا با پشتیبانی تماس بگیرید.",
            reply_to_message_id=update.effective_message.id,
        )
        return

    active_restaurants = await sync_to_async(list)(user.restaurant.all())
    restaurants_list = "رستوران های فعال شما:\n\n"

    for restaurant in active_restaurants:
        restaurants_object = await sync_to_async(getattr)(restaurant, 'restaurant')
        restaurant_name = await sync_to_async(getattr)(restaurants_object, 'restaurant_name')
        restaurants_list += f"{restaurant_name}\n\n"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=restaurants_list,
    )
