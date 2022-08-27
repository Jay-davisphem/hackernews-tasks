import os
from django.conf import settings
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsproject.settings")
app = Celery("newsapp")
app.config_from_object("django.conf:settings", namespace="CELERY")
#app.conf.update(BROKER_URL=os.getenv('CELERY_BROKER_URL'), CELERY_RESULT_BACKEND=os.getenv('CELERY_RESULT_BACKEND'))
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
