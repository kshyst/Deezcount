from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder

from telegram_bot.statics.commands import commands

load_dotenv(dotenv_path='.env')

async def post_init(application):
    await application.bot.set_my_commands(commands)

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).post_init(post_init).build()