import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ruty.settings')

app = Celery('ruty')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()