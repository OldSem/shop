# invitro/celery.py
 
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invitro.settings')
 
app = Celery('invitro')
app.config_from_object('django.conf:settings')


 
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'print_word': {
        'task': 'shop.tasks.hello',
        'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}