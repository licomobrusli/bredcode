from django.core.management.base import BaseCommand
from config.tasks import start_of_day_process, archive_all_time_resource_queue_items

class Command(BaseCommand):
    help = 'Run the start of day process'

    def handle(self, *args, **options):
        archive_all_time_resource_queue_items()
        start_of_day_process()
        self.stdout.write(self.style.SUCCESS('Start of day process executed successfully'))
