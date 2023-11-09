from django.core.management.base import BaseCommand
from config.models import ModalSelect

class Command(BaseCommand):
    help = 'Load a list of service categories into the database'

    def handle(self, *args, **kwargs):
        select_data = [
            ('TOL0', 'Scissors', 'Cut with scissors', 5, 2.50, None, None,'/path/to/diseños/image'),
            ('TOL1', 'Clipper', 'Cut with clippers', 5, 2.50, None, None, '/path/to/otros/image'),
            ('TOL2', 'Cut-throat', 'Cut with razor', 5, 2.50, None, None, '/path/to/otros/image'),
            ('TOL3', 'Babyliss', 'Cut with Babyliss.', 5, 2.50, None, None, '/path/to/otros/image'),
            ('COL0', 'Black', 'Black dye', 5, 2.50, None, None, '/path/to/Black/image'),
            ('COL1', 'Brown', 'Brown dye', 5, 2.50, None, None, '/path/to/Brown/image'),
            ('COL2', 'Red', 'Red dye', 5, 2.50, None, None, '/path/to/Red/image'),
            ('COL3', 'Orange', 'Orange dye', 5, 2.50, None, None, '/path/to/Orange/image'),
            ('COL4', 'Yellow', 'Yellow dye', 5, 2.50, None, None, '/path/to/Yellow/image'),
            ('COL5', 'Blonde', 'Blonde dye', 5, 2.50, None, None, '/path/to/Blonde/image'),
            ('COL6', 'Green', 'Green dye', 5, 2.50, None, None, '/path/to/Green/image'),
            ('COL7', 'Blue', 'Blue dye', 5, 2.50, None, None, '/path/to/Blue/image'),
            ('COL8', 'Purple', 'Purple dye', 5, 2.50, None, None, '/path/to/Purple/image'),
            ('COL9', 'Pink', 'Pink dye', 5, 2.50, None, None, '/path/to/Pink/image'),
            ('DSN0', 'Crown', 'Top of the head', 5, 2.50, None, None, '/path/to/Crown/image'),
            ('DSN1', 'Occiput', 'Back and sides', 5, 2.50, None, None, '/path/to/Occiput/image'),
            ]
        
        for code, name, description, duration, price, category_code, service_code, image_path in select_data:
            # Create ModalSelect instance with fields in the order defined in your model
            ModalSelect.objects.create(
                code=code,
                name=name,
                description=description,
                duration=duration,
                price=price,
                category_code=category_code,
                service_code=service_code,
                image_path=image_path,
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
