from django.db import models
from django.utils import timezone
from django.apps import apps
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date

class ServiceCategory(models.Model):
    code = models.CharField(max_length=5, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    image_path = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'service_categories' # Ensures the table name is exact
        ordering = ['code']  # Default ordering
        verbose_name_plural = 'Service Categories'  # Plural name for the model


class Services(models.Model):
    code = models.CharField(max_length=5, unique=True, primary_key=True)
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
        ordering = ['code']  # Default ordering
        verbose_name = 'Service'

class ModalSelect(models.Model):
    code = models.CharField(max_length=5, unique=True, primary_key=True)
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
        ordering = ['code']  # Default ordering


class SegmentParam(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    container = models.BooleanField(default=False)
    contained = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    working = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    calc_pay = models.IntegerField(default=0)
    calc_available = models.IntegerField(default=0)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        db_table = 'segment_params'
        ordering = ['code']


class Segment(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    type = models.CharField(max_length=100)
    segment_param = models.ForeignKey(SegmentParam, on_delete=models.CASCADE, related_name='segments')

    class Meta:
        db_table = 'segments'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.type}"


class ModalCount(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
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
        ordering = ['code']  # Default ordering

class Orders(models.Model):
    item_count = models.IntegerField()
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    est_start = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    est_duration = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    date_created = models.DateField(auto_now_add=True)
    order_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        creating = not self.id  # Check if the object is being created
        now = timezone.now()

        if creating:
            # Assign est_start, time_created, and date_created before first save
            self.est_start = now.time()
            self.time_created = now.time()
            self.date_created = now.date()

        super(Orders, self).save(*args, **kwargs)

    class Meta:
        db_table = 'orders'
        ordering = ['id']
        verbose_name = 'Order'


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.PROTECT)
    modal_count = models.ForeignKey(ModalCount, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_count = models.IntegerField(blank=True, null=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    est_start = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    est_duration = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
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
        verbose_name = 'Order Item'

class Employee(models.Model):
    resource_item = models.OneToOneField('TimeResourceItems', on_delete=models.CASCADE, related_name='employees', primary_key=True)
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
    resource_model = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.resource_item})"

    @property
    def start_date(self):
        return self.resource_item.start_date if self.resource_item else None

    @property
    def end_date(self):
        return self.resource_item.end_date if self.resource_item else None

    class Meta:
        db_table = 'employees'
        ordering = ['resource_item']


class Equipment(models.Model):
    resource_item = models.OneToOneField('TimeResourceItems', on_delete=models.CASCADE, related_name='equipment', primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    resource_model = models.ForeignKey('ResourceModel', on_delete=models.CASCADE)
    
    # Additional fields can be added here based on your specific requirements
    # Examples: maintenance_schedule, last_maintenance_date, etc.

    def __str__(self):
        return f"{self.name} ({self.resource_item})"

    @property
    def start_date(self):
        return self.resource_item.start_date if self.resource_item else None

    @property
    def end_date(self):
        return self.resource_item.end_date if self.resource_item else None

    class Meta:
        db_table = 'equipment'
        ordering = ['resource_item']

class ResourceType(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    measure = models.CharField(max_length=100)
    unit_size = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        db_table = 'resource_types'
        ordering = ['code']


class ResourceModel(models.Model):
    code = models.CharField(max_length=5, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(ResourceType, on_delete=models.PROTECT, to_field='code')
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_units = models.IntegerField()
    fungible = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code}) - {'Fungible' if self.fungible else 'Non-Fungible'}"

    class Meta:
        db_table = 'resource_models'
        ordering = ['code']


class Phase(models.Model):
    code = models.CharField(max_length=5, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    sequence = models.IntegerField()
    duration = models.IntegerField()
    modal_count = models.ForeignKey('ModalCount', on_delete=models.PROTECT, null=True, blank=True)  # Assuming 'ModalCount' is a model you have defined elsewhere
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'phases'
        ordering = ['code']  # Changed from 'id' to 'code'

class PhaseResource(models.Model):
    code = models.OneToOneField('Segment', on_delete=models.CASCADE, unique=True, primary_key=True, related_name='phase_resource')  # Assuming 'Segment' is a model you have defined elsewhere
    name = models.CharField(max_length=100)
    phase_code = models.ForeignKey(Phase, on_delete=models.PROTECT)
    resource_models_code = models.ForeignKey('ResourceModel', on_delete=models.CASCADE)  # Assuming 'ResourceModel' is a model you have defined elsewhere
    resource_types_code = models.ForeignKey('ResourceType', on_delete=models.CASCADE)  # Assuming 'ResourceType' is a model you have defined elsewhere
    date_created = models.DateField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.code.type != 'PhaseResource':
            raise ValidationError('The Segment instance must have type "PhaseResource"')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'phase_resources'
        ordering = ['code']  # Changed from 'id' to 'code'


class TimeResourcesQueue(models.Model):
    resource_item_code = models.ForeignKey('TimeResourceItems', on_delete=models.CASCADE)
    segment = models.ForeignKey('Segment', on_delete=models.CASCADE, related_name='time_resources_queue')
    segment_name = models.CharField(max_length=100)
    segment_start = models.DateTimeField()
    segment_end = models.DateTimeField()
    staff_start = models.DateTimeField(blank=True, null=True)
    staff_end = models.DateTimeField(blank=True, null=True)
    staff_timer = models.DurationField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    resource_model = models.ForeignKey('ResourceModel', on_delete=models.CASCADE)
    segment_params = models.ForeignKey('SegmentParam', on_delete=models.PROTECT)
    order_number = models.ForeignKey(Orders, on_delete=models.PROTECT, null=True, blank=True, to_field='order_number')


    def __str__(self):
        return f"{self.resource_item_code} ({self.segment})"

    class Meta:
        db_table = 'time_resources_queue'
        ordering = ['id']


class TimeResourcesQueueHistory(models.Model):
    original_id = models.IntegerField()
    resource_item_code = models.ForeignKey('TimeResourceItems', on_delete=models.CASCADE)
    segment = models.CharField(max_length=50)
    segment_name = models.CharField(max_length=100, blank=True, null=True)
    segment_start = models.DateTimeField()
    segment_end = models.DateTimeField()
    staff_start = models.DateTimeField(blank=True, null=True)
    staff_end = models.DateTimeField(blank=True, null=True)
    date_created = models.DateField()
    resource_model = models.ForeignKey(ResourceModel, on_delete=models.CASCADE)
    segment_params = models.ForeignKey('SegmentParam', on_delete=models.PROTECT, null=True, blank=True)
    archived_date = models.DateTimeField(auto_now_add=True)  # Date when the record was archived
    order_number = models.ForeignKey(Orders, on_delete=models.PROTECT, null=True, blank=True, to_field='order_number')
    
    def __str__(self):
        return f"{self.resource_item_code} ({self.segment}) - Archived"

    class Meta:
        db_table = 'time_resources_queue_history'
        ordering = ['archived_date']


class ResourceAvailability(models.Model):
    resource_item = models.ForeignKey('TimeResourceItems', on_delete=models.CASCADE)
    resource_model = models.ForeignKey('ResourceModel', on_delete=models.CASCADE)
    available_start = models.DateTimeField()
    available_end = models.DateTimeField()
    duration = models.DurationField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource_item} available from {self.available_start} to {self.available_end}"

    class Meta:
        db_table = 'resource_availablity'
        ordering = ['date_created', 'available_start']


class ScheduleTemplateIndex(models.Model):
    code = models.CharField(max_length=5, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    rotations = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'schedule_template_index'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class ScheduleTemplate(models.Model):
    index_code = models.ForeignKey(ScheduleTemplateIndex, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, unique=True, primary_key=True)
    wk = models.CharField(max_length=1)
    wkday = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    sched_container = models.DurationField()
    lunch_duration = models.DurationField(null=True, blank=True)
    gross_sched = models.DurationField()
    breaks_duration = models.DurationField(null=True, blank=True)
    net_sched = models.DurationField()
    date_created = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate the duration between shift_start and shift_end
        self.sched_container = datetime.combine(datetime.min, self.shift_end) - \
                               datetime.combine(datetime.min, self.shift_start)

        # Calculate gross_sched by subtracting lunch_duration from sched_container
        self.gross_sched = self.sched_container - (self.lunch_duration or timedelta())

        # Calculate net_sched by subtracting breaks_duration from gross_sched
        self.net_sched = self.gross_sched - (self.breaks_duration or timedelta())

        super(ScheduleTemplate, self).save(*args, **kwargs)

    class Meta:
        db_table = 'schedule_templates'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.wk} - {self.wkday}"


class TimeResourceScheduleIndex(models.Model):
    resource_item = models.ForeignKey('TimeResourceItems', on_delete=models.CASCADE)
    schedule_index = models.ForeignKey('ScheduleTemplateIndex', on_delete=models.CASCADE)
    resource_model = models.ForeignKey('ResourceModel', on_delete=models.CASCADE)
    first_rotation = models.CharField(max_length=1)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'time_resource_schedule_index'  # Replace with your actual table name

    def __str__(self):
        return f"{self.id} - {self.resource_item} - {self.schedule_index}"
    

class TimeResourceItems(models.Model):
    resource_item_code = models.CharField(max_length=25, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(blank=True, null=True)
    resource_model = models.ForeignKey('ResourceModel', on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'time_resource_items'
        ordering = ['resource_item_code']
        unique_together = [['resource_item_code', 'start_date', 'end_date']]  # Unique constraint

    def __str__(self):
        return f"{self.name} ({self.resource_item_code})"
    
class ScheduleElements(models.Model):
    code = models.OneToOneField(Segment, on_delete=models.CASCADE, primary_key=True, related_name='schedule_elements')
    name = models.CharField(max_length=25)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.code.type != 'ScheduleElements':
            raise ValidationError('The Segment instance must have type "ScheduleElements"')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'schedule_elements'  # Ensures the table name is exactly 'schedule_elements'
        ordering = ['code']  # Default ordering

class EmployeePhases(models.Model):
    employee_phase = models.CharField(max_length=255, unique=True, primary_key=True)
    resource_item_code = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_phases')
    resource_model_id = models.ForeignKey(ResourceModel, on_delete=models.CASCADE, related_name='employee_phases')
    phase_resource_id = models.ForeignKey(PhaseResource, on_delete=models.CASCADE, related_name='employee_phases')
    avg_duration = models.IntegerField(null=True, blank=True)
    avg_score = models.FloatField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'employee_phases'  # Ensures the table name is exactly 'employee_phases'
        ordering = ['employee_phase']  # Default ordering

    def __str__(self):
        return self.employee_phase
