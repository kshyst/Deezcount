from asgiref.sync import sync_to_async
from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import os
import django

from telegram_bot import get_restaurant_list

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_base.settings")
django.setup()

from telegram_user.models import User, AvailableRestaurant, ActiveRestaurant
from app import app
from tasks import send_bulk_discounts

ENTRY, RESTAURANT_NAME, SELECT_RESTAURANT = range(3)


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text= update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
    )

    if not await sync_to_async(User.objects.filter(telegram_id=update.effective_chat.id).exists)():
        user = User(telegram_id=update.effective_chat.id, telegram_username=update.effective_chat.username)
        name = update.effective_chat.first_name + " " + update.effective_chat.last_name if update.effective_chat.last_name else update.effective_chat.first_name
        user.telegram_account_name = name

        await sync_to_async(user.save)()

    send_bulk_discounts.delay()

async def send_restaurant_search_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="نام رستوران مورد نظر خود را وارد کنید.",
        reply_to_message_id=update.effective_message.id,
    )
    return RESTAURANT_NAME

async def show_restaurant_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    search_query = update.message.text
    restaurant_list = get_restaurant_list(search_query)
    context.user_data['restaurant_list'] = restaurant_list

    if not restaurant_list:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="رستورانی با این نام پیدا نشد. لطفا دوباره تلاش کنید.",
            reply_to_message_id=update.effective_message.id,
        )
        return RESTAURANT_NAME
    else:
        message = "رستوران های پیدا شده:\n"

        for restaurant in restaurant_list:
            num = restaurant.get("number")
            title = restaurant.get("title")
            message += f"{num} - {title}\n\n"

        message += "لطفا شماره رستوران مورد نظر خود را ارسال کنید."

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
        return SELECT_RESTAURANT

async def select_restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    restaurant_num = update.message.text

    try:
        restaurant_number = int(restaurant_num)
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="لطفا یک شماره معتبر وارد کنید.",
            reply_to_message_id=update.effective_message.id,
        )
        return SELECT_RESTAURANT

    if restaurant_number not in range(1, len(context.user_data['restaurant_list']) + 1):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="لطفا یک شماره معتبر وارد کنید.",
            reply_to_message_id=update.effective_message.id,
        )
        return SELECT_RESTAURANT

    restaurant = context.user_data['restaurant_list'][restaurant_number - 1]

    restaurant_name = restaurant.get("title")
    restaurant_code = restaurant.get("code")

    if not await sync_to_async(AvailableRestaurant.objects.filter(restaurant_code=restaurant_code).exists)():
        restaurant_object = AvailableRestaurant(restaurant_name=restaurant_name, restaurant_code=restaurant_code)
        await sync_to_async(restaurant_object.save)()

        restaurant_active_object = ActiveRestaurant(restaurant=restaurant_object)
        await sync_to_async(restaurant_active_object.save)()
    else:
        restaurant_object = await sync_to_async(AvailableRestaurant.objects.get)(restaurant_code=restaurant_code)
        restaurant_active_object = await sync_to_async(ActiveRestaurant.objects.get)(restaurant=restaurant_object)

    user = await sync_to_async(User.objects.get)(telegram_id=update.effective_chat.id)
    await sync_to_async(user.restaurant.add)(restaurant_active_object)
    await sync_to_async((await sync_to_async(User.objects.get)(telegram_id=update.effective_chat.id)).save)()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"شما رستوران {restaurant_name} را انتخاب کردید.",
        reply_to_message_id=update.effective_message.id,
    )
    return ConversationHandler.END

if __name__ == "__main__":
    app.add_handler(CommandHandler("start", start_command_handler))

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("restaurant", send_restaurant_search_query)],
        states={
            ENTRY: [
                CommandHandler("restaurant", send_restaurant_search_query),
            ],
            RESTAURANT_NAME: [
                MessageHandler(filters.TEXT, show_restaurant_list),
            ],
            SELECT_RESTAURANT: [
                MessageHandler(filters.TEXT, select_restaurant),
            ]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END),],
        allow_reentry=False,
    ))

    app.run_polling()