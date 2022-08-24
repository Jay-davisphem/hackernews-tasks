import sys
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from newsapp.utils import scheduled_tasks1


class Command(BaseCommand):
    help = "Scheduled data fetching from hackernews for every 5 minutes"

    def handle(self, *args, **options):
        scheduled_tasks1()
