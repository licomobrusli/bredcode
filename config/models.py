from django.db import models
from django.utils import timezone
import random
import string

class ServiceCategory(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    image_path = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'service_categories' # Ensures the table name is exact
        ordering = ['id']  # Default ordering


class Services(models.Model):
    code = models.CharField(max_length=4, unique=True)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    total_duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_path = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'services' # Ensures the table name is exact
        ordering = ['id']  # Default ordering

class ModalSelect(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_code = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, null=True, blank=True)
    service_code = models.ForeignKey(Services, on_delete=models.PROTECT, null=True, blank=True)
    image_path = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'modal_select'  # Ensures the table name is exactly 'modal_select'
        ordering = ['id']  # Default ordering


class ModalCount(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_quantity = models.IntegerField()
    category_code = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, null=True, blank=True)
    service_code = models.ForeignKey(Services, on_delete=models.PROTECT, null=True, blank=True)
    image_path = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    logic = models.CharField(max_length=3, default='NOT', null=False)
    sub = models.IntegerField(default=0, null=False)
    sequence = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'modal_count'  # Ensures the table name is exactly 'ModalCount'
        ordering = ['id']  # Default ordering

class Orders(models.Model):
    item_count = models.IntegerField()
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    est_start = models.TimeField(auto_now_add=True, blank=True, null=True)
    est_duration = models.IntegerField(blank=True, null=True)
    start = models.TimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    time_created = models.TimeField(auto_now_add=True)
    date_created = models.DateField(auto_now_add=True)
    order_number = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        creating = not self.id  # Check if the object is being created
        now = timezone.now()

        if creating:
            # Assign est_start, time_created, and date_created before first save
            self.est_start = now.time()
            self.time_created = now.time()
            self.date_created = now.date()

        super(Orders, self).save(*args, **kwargs)

        if creating:
            # Generate and assign order_number after the object has been saved
            franchise_code = 'M1'
            date_str = now.strftime('%y%m%d%H')
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
            self.order_number = f"{franchise_code}{date_str}{str(self.id).zfill(6)}{random_str}"
            super(Orders, self).save(update_fields=['order_number'])

    class Meta:
        db_table = 'orders'
        ordering = ['id']

class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.PROTECT)
    modal_count = models.ForeignKey(ModalCount, on_delete=models.PROTECT, null=True, blank=True)
    item_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_count = models.IntegerField(blank=True, null=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    est_start = models.TimeField(auto_now_add=True, blank=True, null=True)
    est_duration = models.IntegerField(blank=True, null=True)
    start = models.TimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    time_created = models.TimeField(auto_now_add=True)
    date_created = models.DateField(auto_now_add=True)
    order_number = models.CharField(max_length=20, unique=False, blank=True)

    def save(self, *args, **kwargs):
        # If the object is being created, assign time and date fields
        if not self.id:
            now = timezone.now()
            self.est_start = now.time()
            self.time_created = now.time()
            self.date_created = now.date()

        # Before saving, check if 'order' is set and use its 'order_number'
        if self.order and not self.order_number:
            self.order_number = self.order.order_number

        super(OrderItems, self).save(*args, **kwargs)

    class Meta:
        db_table = 'order_items'
        ordering = ['id']


class Employee(models.Model):
    code = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    dni = models.CharField(max_length=10, unique=True)
    naf = models.CharField(max_length=15, unique=True)
    dob = models.DateField()
    tel = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.code})"

    class Meta:
        db_table = 'employees'
        ordering = ['id']


class ResourceType(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    measure = models.CharField(max_length=100)
    unit_size = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        db_table = 'resource_types'
        ordering = ['id']


class ResourceModel(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(ResourceType, on_delete=models.PROTECT, to_field='code')
    type_code = models.CharField(max_length=5)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_units = models.IntegerField()
    fungible = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure the type_code is set to the code of the related ResourceType
        if not self.type_code:
            self.type_code = self.type.code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code}) - {'Fungible' if self.fungible else 'Non-Fungible'}"

    class Meta:
        db_table = 'resource_models'
        ordering = ['id']

from django.db import models

class Phase(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    item_code = models.ForeignKey(ModalCount, on_delete=models.PROTECT)
    sequence = models.IntegerField()
    duration = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'phases'
        ordering = ['id']

from django.db import models

class PhaseResource(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    phase_code = models.ForeignKey(Phase, on_delete=models.PROTECT)
    resource_models_code = models.ForeignKey(ResourceModel, on_delete=models.PROTECT)
    resource_types_code = models.ForeignKey(ResourceType, on_delete=models.PROTECT, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'phase_resources'
        ordering = ['id']


class TimeResourcesQueue(models.Model):
    resource_item_code = models.CharField(max_length=25)
    resource_item_name = models.CharField(max_length=100)
    segment_type = models.IntegerField()  # Assuming segment_type is an integer that refers to a type
    segment = models.CharField(max_length=50)  # 'segment' field to describe the type like 'shift_container' or 'break'
    segment_start = models.TimeField()
    segment_end = models.TimeField()
    date_created = models.DateField(auto_now_add=True)
    resource_model_id = models.ForeignKey(ResourceModel, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.resource_item_name} ({self.segment})"

    class Meta:
        db_table = 'time_resources_queue'  # This is to ensure the table name in the database matches the provided name
