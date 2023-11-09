from django.core.management.base import BaseCommand
from django.db import connection
from config.models import Services

class Command(BaseCommand):
    help = 'Replaces the services in the database with new data'

    def handle(self, *args, **kwargs):
        # Truncate the table
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE services RESTART IDENTITY CASCADE;')
            self.stdout.write(self.style.SUCCESS('Table truncated successfully'))

        # New data to be inserted into the 'services' table
        new_services_data = [
            ('CUT', 'HED', 'Cut', 'Various styles of haircuts and trims.', 20, 10.00, '/path/to/cut/image'),
            ('COL', None, 'Colour', 'Hair coloring services including full color, highlights, and more.', 60, 30.00, '/path/to/colour/image'),
            ('DSN', None, 'Design', 'Intricate designs or patterns for hair and beard.', 10, 5.00, '/path/to/design/image'),
        ]

        # Insert new data
        for code, service_category, name, description, total_duration, price, image_path in new_services_data:
            Services.objects.create(
                code=code,
                service_category=service_category,
                name=name,
                total_duration=total_duration,
                price=price,
                description=description,
                image_path=image_path,
            )
        self.stdout.write(self.style.SUCCESS('New data imported successfully'))
