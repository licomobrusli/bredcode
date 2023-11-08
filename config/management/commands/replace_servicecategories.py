from django.core.management.base import BaseCommand
from django.db import connection
from config.models import ServiceCategory

class Command(BaseCommand):
    help = 'Replaces the service categories in the database with new data'

    def handle(self, *args, **kwargs):
        # Truncate the table
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE service_categories RESTART IDENTITY CASCADE;')
            self.stdout.write(self.style.SUCCESS('Table truncated successfully'))

        # New data to be inserted
        service_categories = [
            ('HED', 'Head', 'The scalp. El cuero cabelludo.', '/path/to/head/image'),
            ('FCE', 'Face', 'Eyes, ears & nose. Ojos, oidos y nariz.', '/path/to/face/image'),
            ('BRD', 'Beard', 'The facial hair.  El vello facial.', '/path/to/beard/image'),
        ]

        # Insert new data
        for code, name, description, image_path in service_categories:
            ServiceCategory.objects.create(
                code=code,
                name=name,
                description=description,
                image_path=image_path,
            )
        self.stdout.write(self.style.SUCCESS('New data imported successfully'))
