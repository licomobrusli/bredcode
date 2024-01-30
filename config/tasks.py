from django.utils import timezone
from django.db.models import F, Q, Func
from django.db.models.functions import Now, ExtractWeekDay
from django.db import transaction
from config.models import TimeResourcesQueue, EmployeeScheduleIndex, ResourceModel, SegmentParam, ScheduleTemplate
import datetime

def start_of_day_process():

    # Fetch current date
    current_date = timezone.now().date()

    # Fetch your data
    employee_schedules = (
        EmployeeScheduleIndex.objects
        .filter(
            Q(end_date__isnull=True) | Q(end_date__gte=Func(Now(), function='DATE')),
            start_date__lte=Func(Now(), function='DATE'),
            schedule_templates__wkday=ExtractWeekDay(Now())  # Adjust as needed
        )
        .annotate(
            shift_start=F('schedule_templates__shift_start'),
            shift_end=F('schedule_templates__shift_end'),
            employee_code=F('employee__code'),
            resource_model_code=F('resource_model__code'),
        )
        .values(
            'shift_start', 'shift_end', 'employee_code', 
            'resource_model_code'
        )
    )

    # Prefetch ResourceModel instances
    resource_model_codes = [es['resource_model_code'] for es in employee_schedules]
    resource_models = ResourceModel.objects.filter(code__in=resource_model_codes).in_bulk(field_name='code')

    # Get the SegmentParam instance for 'CNTN' code
    segment_param = SegmentParam.objects.get(code='CNTN')

    # Prepare the data for bulk_create
    time_resource_queue_objects = [
        TimeResourcesQueue(
            resource_item_code=es['employee_code'],
            segment_start=datetime.datetime.combine(current_date, es['shift_start']),  # Combine date and time
            segment_end=datetime.datetime.combine(current_date, es['shift_end']),  # Combine date and time
            date_created=timezone.now(),
            resource_model=resource_models.get(es['resource_model_code']),  # Refer to the prefetched ResourceModel instance
            segment_params=segment_param,  # Assign the 'CNTN' SegmentParam instance
        )
        for es in employee_schedules if es['resource_model_code'] in resource_models  # Ensure the code exists in the prefetched data
    ]

    # Use Django's bulk_create to insert all records in a single query within a transaction
    with transaction.atomic():
        TimeResourcesQueue.objects.bulk_create(time_resource_queue_objects)
