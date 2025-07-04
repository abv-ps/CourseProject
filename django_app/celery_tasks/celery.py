import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')

# app = Celery('my_celery')

app = Celery('my_celery', include=['django_app.celery_tasks.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks(['celery_tasks'])

app.conf.beat_schedule = {
    'log-users-every-10-minutes': {
        'task': 'django_app.celery_tasks.tasks.log_total_users',
        'schedule': crontab(minute='*/10'),
    },
}
