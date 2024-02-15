import csv
from django.core.exceptions import ObjectDoesNotExist
from config.models import ModalCount, Segment, ServiceCategory, Services
from django.db import transaction

def load_csv_to_model(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        with transaction.atomic():
            for row in reader:
                segment, _ = Segment.objects.get_or_create(id=row['code'])
                category_code = None
                if row['category_code']:
                    category_code, _ = ServiceCategory.objects.get_or_create(id=row['category_code'])
                service_code = None
                if row['service_code']:
                    service_code, _ = Services.objects.get_or_create(id=row['service_code'])

                ModalCount.objects.create(
                    code=segment,
                    name=row['name'],
                    description=row['description'],
                    duration=int(row['duration']),
                    price=row['price'],
                    max_quantity=int(row['max_quantity']),
                    category_code=category_code,
                    service_code=service_code,
                    image_path=row['image_path'],
                    logic=row['logic'],
                    sub=int(row['sub']),
                    sequence=(int(row['sequence']) if row['sequence'] else None),
                )

if __name__ == '__main__':
    load_csv_to_model('C:\Users\leejh\Documents\ModalCountData.csv')
