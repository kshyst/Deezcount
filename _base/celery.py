import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_base.settings')


celery_app = Celery('deezcount', broker=os.getenv('CELERY_BROKER_URL'))
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'send-discounts-every-15-min': {
        'task': 'tasks.send_bulk_discounts',
        'schedule': 10 * 60,
    },
}