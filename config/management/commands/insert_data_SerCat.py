from django.core.management.base import BaseCommand
from config.models import ServiceCategory

class Command(BaseCommand):
    help = 'Load a list of service categories into the database'

    def handle(self, *args, **kwargs):
        service_categories = [
            ('CRT', 'Cortes', 'Various styles of haircuts and trims.', '/path/to/cortes/image'),
            ('TNT', 'Tintes', 'Hair coloring services including full color, highlights, and more.', '/path/to/tintes/image'),
            ('DSN', 'Diseños', 'Intricate designs or patterns for hair and beard.', '/path/to/diseños/image'),
            ('OTR', 'Otros', 'Other miscellaneous services.', '/path/to/otros/image'),
        ]

        for code, name, description, image_path in service_categories:
            ServiceCategory.objects.create(
                code=code,
                name=name,
                description=description,
                image_path=image_path,
            )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
