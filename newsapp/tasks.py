from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from .utils import scheduled_tasks1


def start():
    """
    Entry point for tasks scheduling.
    Schedule to run once and every 5 minutes
    it's started in ```newsproject/urls.py```
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_tasks1)  # Job runs once
    scheduler.add_job(
        scheduled_tasks1, "interval", minutes=5
    )  # Job runs every five minutes
    scheduler.start()
