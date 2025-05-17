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
)

from telegram_user.models import User
from telegram_bot.statics.reply_keyboards import main_menu_buttons


async def change_bot_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    telegram_user = await sync_to_async(User.objects.get)(telegram_id=update.effective_user.id)
    user_does_want_notifications = await sync_to_async(lambda : telegram_user.does_want_notifications)()
    await sync_to_async(telegram_user.change_status)()

    if user_does_want_notifications:
        message = "تخفیف یاب متوقف شد."
    else:
        message = "تخفیف یاب روشن شد."

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_to_message_id=update.effective_message.id,
        reply_markup=ReplyKeyboardMarkup(
            main_menu_buttons, one_time_keyboard=True
        ),
    )
