import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_base.settings')


celery_app = Celery('deezcount', broker='redis://localhost:6379/0')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.broker_connection = 'redis://localhost:6379/0'

celery_app.conf.beat_schedule = {
    'send-discounts-every-15-min': {
        'task': 'tasks.send_bulk_discounts',
        'schedule': 10,
    },
}