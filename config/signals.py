from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import TimeResourcesQueue, ResourceAvailability, Employee, PhaseResource, EmployeePhases
import logging
from prettytable import PrettyTable
from config.time_utils import now_minutes

# Create a logger instance
logger = logging.getLogger(__name__)

@receiver(post_save, sender=TimeResourcesQueue)
@receiver(post_delete, sender=TimeResourcesQueue)
@transaction.atomic
def update_resource_availability(sender, instance, **kwargs):
    # Delete existing ResourceAvailability records for the resource_item_code
    ResourceAvailability.objects.filter(resource_item=instance.resource_item_code).delete()
    logger.info(f"Deleted ResourceAvailability for {instance.resource_item_code}")

    # Fetch all container segments for the resource item
    containers = TimeResourcesQueue.objects.filter(
        resource_item_code=instance.resource_item_code,
        segment_params__container=True
    ).order_by('segment_start')

    # Initialize a list to keep track of non-overlapping available periods
    available_periods = []

    # Iterate through each container to find and calculate its available periods
    for container in containers:
        # Start with the container's own time as the initial available period
        period_start = container.segment_start
        period_end = container.segment_end

        # Get all overlapping segments excluding other containers
        overlapping_segments = TimeResourcesQueue.objects.filter(
            resource_item_code=container.resource_item_code,
            segment_end__gt=container.segment_start,
            segment_start__lt=container.segment_end
        ).exclude(
            segment_params__container=True
        ).order_by('segment_start')

        # Split the container's time into available periods around the overlapping segments
        for segment in overlapping_segments:
            # If the overlapping segment starts after the current period start,
            # then we have found an available period before the overlap occurs.
            if segment.segment_start > period_start:
                available_periods.append((period_start, segment.segment_start))

            # Update period_start to the end of the overlapping segment,
            # effectively 'removing' the overlap from the available time.
            period_start = max(period_start, segment.segment_end)

        # After processing all overlapping segments, if the last segment's end
        # is before the container's end, add the remaining time as available.
        if period_start < period_end:
            available_periods.append((period_start, period_end))

    # Update ResourceAvailability Table based on calculated available periods
    for start, end in available_periods:
        duration = end - start  # Calculate the duration based on updated start and end times
        ResourceAvailability.objects.create(
            resource_item=instance.resource_item_code,
            resource_model=container.resource_model,
            available_start=start,
            available_end=end,
            duration=duration
        )
        logger.info(f"ResourceAvailability record created: Start {start}, End {end}, for {instance.resource_item_code}")

@receiver(post_save, sender=Employee)
def create_employee_phases(sender, instance, created, **kwargs):
    if created:
        employee_phases_list = []  # List to hold instances for bulk creation
        phase_resources = PhaseResource.objects.filter(resource_models_code=instance.resource_model)

        for phase_resource in phase_resources:
            # Create an EmployeePhases instance and add it to the list
            employee_phases_instance = EmployeePhases(
                resource_item_code=instance,  # Directly use the Employee instance
                phase_resource_id=phase_resource,  # Directly use the PhaseResource instance
                employee_phase=f"{instance.id}_{phase_resource.id}",  # Construct employee_phase string based on IDs
                resource_model_id=phase_resource.resource_models_code,  # Set this field as in the original logic
                # Add other necessary fields as needed
            )
            employee_phases_list.append(employee_phases_instance)
        
        # Use bulk_create to save all new EmployeePhases instances at once
        with transaction.atomic():  # Ensure database integrity
            EmployeePhases.objects.bulk_create(employee_phases_list)
