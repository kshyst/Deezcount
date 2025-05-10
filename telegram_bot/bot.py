from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)

from app import app
from tasks import send_bulk_discounts

async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text= update.effective_chat.id,
        reply_to_message_id=update.effective_message.id,
    )

    send_bulk_discounts.delay()

if __name__ == "__main__":
    app.add_handler(CommandHandler("start", start_command_handler))

    app.run_polling()