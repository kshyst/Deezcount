source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver &
# Start the Telegram bot
PYTHONUNBUFFERED=1 DJANGO_SETTINGS_MODULE=_base.settings python -m telegram_bot.bot &
# Start Celery workers and beat scheduler
celery -A _base.celery worker -l info
celery -A _base.celery beat -l info