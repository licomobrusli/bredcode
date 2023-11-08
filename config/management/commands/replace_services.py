from django.core.management.base import BaseCommand
from django.db import connection
from config.models import services

class Command(BaseCommand):
    help = 'Replaces the services in the database with new data'

    def handle(self, *args, **kwargs):
        # Truncate the table
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE services RESTART IDENTITY CASCADE;')
            self.stdout.write(self.style.SUCCESS('Table truncated successfully'))

         # New data to be inserted
        service_categories = [
            ('CUT', 'Cut', 'Various styles of haircuts and trims.', '20', '10', '/path/to/cut/image'),
            ('COL', 'Colour', 'Hair coloring services including full color, highlights, and more.', '60', '30', '/path/to/colour/image'),
            ('DSN', 'Design', 'Intricate designs or patterns for hair and beard.', '10', '5', '/path/to/design/image'),
        ]

        # Insert new data
        for code, name, description, total_duration, price, image_path in services:
            services.objects.create(
                code=code,
                name=name,
                total_duration=total_duration,
                price=price,
                description=description,
                image_path=image_path,
            )
        self.stdout.write(self.style.SUCCESS('New data imported successfully'))
 