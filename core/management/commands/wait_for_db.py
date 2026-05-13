import time

from django.core.management import BaseCommand
from django.db import connections, OperationalError


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for database...")
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections["default"]
                db_conn.cursor()
            except OperationalError:
                self.stdout.write("Waiting for database...")
                time.sleep(1)
        self.stdout.write("Database connected.")
