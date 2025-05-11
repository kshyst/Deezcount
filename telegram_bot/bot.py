from asgiref.sync import sync_to_async
from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_base.settings")
django.setup()

from telegram_user.models import User
from app import app
from tasks import send_bulk_discounts


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

if __name__ == "__main__":
    app.add_handler(CommandHandler("start", start_command_handler))
    app.run_polling()