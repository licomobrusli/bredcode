from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import TimeResourcesQueue, ResourceAvailability
import logging

# Create a logger instance
logger = logging.getLogger(__name__)

@receiver(post_save, sender=TimeResourcesQueue)
@receiver(post_delete, sender=TimeResourcesQueue)
@transaction.atomic
def update_resource_availability(sender, instance, **kwargs):
    logger.info(f"Signal received for {sender.__name__} with instance {instance.pk}")
    
    # Delete existing ResourceAvailability records for the resource_item_code
    ResourceAvailability.objects.filter(resource_item=instance.resource_item_code).delete()
    logger.info(f"Deleted ResourceAvailability records for {instance.resource_item_code}")

    containers = TimeResourcesQueue.objects.select_for_update().filter(
        resource_item_code=instance.resource_item_code,  # Use the specific resource item code
        segment_params__container=True
    )
    logger.info(f"Containers found: {containers}")

    for container in containers:
        available_periods = [(container.segment_start, container.segment_end)]

        overlapping_segments = TimeResourcesQueue.objects.select_for_update().filter(
            resource_item_code=container.resource_item_code,
            segment_start__lt=container.segment_end,
            segment_end__gt=container.segment_start,
        ).exclude(
            segment_params__container=True
        )
        logger.info(f"Overlapping segments found: {overlapping_segments}")

        for segment in overlapping_segments:
            updated_periods = []
            for start, end in available_periods:
                if segment.segment_start <= start and segment.segment_end >= end:
                    # The overlapping segment completely covers the period
                    continue
                if segment.segment_start > start and segment.segment_end < end:
                    # The overlapping segment splits the period into two
                    updated_periods.append((start, segment.segment_start))
                    updated_periods.append((segment.segment_end, end))
                elif segment.segment_start > start:
                    # The overlapping segment cuts the end of the period
                    updated_periods.append((start, segment.segment_start))
                elif segment.segment_end < end:
                    # The overlapping segment cuts the beginning of the period
                    updated_periods.append((segment.segment_end, end))
            available_periods = updated_periods
        logger.info(f"Available periods: {available_periods}")

        # Update ResourceAvailability Table
        for start, end in available_periods:
            duration = end - start
            ResourceAvailability.objects.create(
                resource_item=container.resource_item_code,
                resource_model=container.resource_model,
                available_start=start,
                available_end=end,
                duration=duration
            )
        logger.info(f"ResourceAvailability records created for {container.resource_item_code}")