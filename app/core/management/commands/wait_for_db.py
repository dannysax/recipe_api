import time
from django.core.management import BaseCommand
from psycopg2 import OperationalError as psycopg2OpError
from django.db.utils import OperationalError





class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # pass
        db_ready = False
        while not db_ready:
            try:
                self.check(databases=["default"])
                db_ready = True
                self.stdout.write(self.style.SUCCESS("database connection successful")) 
            except (psycopg2OpError, OperationalError):
                self.stdout.write("Database not ready. Waiting for 1 second")
                time.sleep(1)
