from django.core.management.base import BaseCommand
from config.tasks import start_of_day_process  # Import your start of day process function

class Command(BaseCommand):
    help = 'Run the start of day process'

    def handle(self, *args, **options):
        # Call your start of day process function
        start_of_day_process()
        self.stdout.write(self.style.SUCCESS('Start of day process executed successfully'))
