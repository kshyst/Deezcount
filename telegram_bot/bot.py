import os

import django
from asgiref.sync import sync_to_async
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from telegram_bot.menus.show_active_restaurants import show_active_restaurants
from telegram_bot.statics.commands import Commands
from telegram_bot.statics.menu_ranges import RESTAURANT_NAME, SELECT_RESTAURANT, ENTRY
from telegram_bot.statics.reply_keyboards import main_menu_buttons

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_base.settings")
django.setup()

from telegram_user.models import User
from app import app
from tasks import send_bulk_discounts

from telegram_bot.menus.submit_restaurant import (
    send_restaurant_search_query,
    show_restaurant_list,
    select_restaurant,
)


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
        reply_markup=ReplyKeyboardMarkup(main_menu_buttons, one_time_keyboard=True
        ),
    )

    if not await sync_to_async(User.objects.filter(telegram_id=update.effective_chat.id).exists)():
        user = User(telegram_id=update.effective_chat.id, telegram_username=update.effective_chat.username)
        name = update.effective_chat.first_name + " " + update.effective_chat.last_name if update.effective_chat.last_name else update.effective_chat.first_name
        user.telegram_account_name = name

        await sync_to_async(user.save)()

    send_bulk_discounts.delay()


if __name__ == "__main__":
    app.add_handler(CommandHandler("start", start_command_handler))
    app.add_handler(MessageHandler(filters.Text(Commands.ACTIVE_RESTAURANT.value), show_active_restaurants))
    app.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("restaurant", send_restaurant_search_query),
            MessageHandler(filters.Text(Commands.ADD_RESTAURANT.value), send_restaurant_search_query),
        ],
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