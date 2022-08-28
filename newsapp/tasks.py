from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from .utils import scheduled_tasks1


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_tasks1, "interval", minutes=5)
    scheduler.start()
