import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsproject.settings")
app = Celery("newsapp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
