from django.utils import timezone
from django.db.models import F, Q, Func
from django.db.models.functions import Now, ExtractWeekDay
from django.db import transaction
from config.models import TimeResourcesQueue, TimeResourcesQueueHistory, EmployeeScheduleIndex, ResourceModel, SegmentParam, ScheduleTemplate
import datetime


def archive_all_time_resource_queue_items():
    with transaction.atomic():
        # Retrieve all items
        items = TimeResourcesQueue.objects.all()

        for item in items:
            # Create a new historical record for each item
            TimeResourcesQueueHistory.objects.create(
                original_id=item.id,
                resource_item_code=item.resource_item_code,
                segment=item.segment,
                segment_start=item.segment_start,
                segment_end=item.segment_end,
                date_created=item.date_created,
                resource_model=item.resource_model,
                segment_params=item.segment_params,
            )
            # Delete the item from the active table
            item.delete()
        
        print(f"Archived {items.count()} items from TimeResourcesQueue.")


def start_of_day_process():
    current_date = timezone.now().date()
    week_of_year = current_date.isocalendar()[1]

    # Fetch employee schedules
    employee_schedules = EmployeeScheduleIndex.objects.filter(
        Q(end_date__isnull=True) | Q(end_date__gte=current_date),
        start_date__lte=current_date,
    ).select_related('schedule_index')

    # Prepare the data for bulk_create
    time_resource_queue_objects = []

    for es in employee_schedules:
        # Calculate the offset for the employee's schedule
        total_rotations = es.schedule_index.rotations
        rotation_start_index = alpha_to_numeric(es.first_rotation)
        current_schedule_index = (week_of_year - 1) % total_rotations
        emp_schedule_index = (rotation_start_index + current_schedule_index) % total_rotations
        emp_current_schedule_code = numeric_to_alpha(emp_schedule_index)

        # Fetch the corresponding schedule template
        schedule_template = ScheduleTemplate.objects.filter(
            index_code=es.schedule_index,
            wk=emp_current_schedule_code,
            wkday=ExtractWeekDay(Now())
        ).first()

        if schedule_template:
            # Create TimeResourcesQueue object
            time_resource_queue_object = TimeResourcesQueue(
                resource_item_code=es.employee.code,
                segment_start=timezone.make_aware(datetime.datetime.combine(current_date, schedule_template.shift_start)),
                segment_end=timezone.make_aware(datetime.datetime.combine(current_date, schedule_template.shift_end)),
                date_created=timezone.now(),
                resource_model=es.resource_model,
                segment_params=SegmentParam.objects.get(code='CNTN'),
            )
            time_resource_queue_objects.append(time_resource_queue_object)

    # Use Django's bulk_create to insert all records
    with transaction.atomic():
        TimeResourcesQueue.objects.bulk_create(time_resource_queue_objects)

def alpha_to_numeric(alpha):
    return ord(alpha.upper()) - ord('A')

def numeric_to_alpha(numeric):
    return chr(ord('A') + numeric)