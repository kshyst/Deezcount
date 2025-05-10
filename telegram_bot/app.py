from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder

load_dotenv(dotenv_path='.env')
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()