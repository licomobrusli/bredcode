# tests.py
from django.test import TestCase
from .models import TimeResourcesQueue, ResourceModel, SegmentParam, ResourceType, ResourceAvailability
from django.utils import timezone
from datetime import timedelta

class TimeResourcesQueueSignalTest(TestCase):
    def setUp(self):
        # Create a ResourceType instance
        resource_type = ResourceType.objects.create(
            code='T',
            name='Test Resource Type',
            measure='Unit',
            unit_size=1
        )

        # Create ResourceModel instance
        resource_model = ResourceModel.objects.create(
            code='RM123',
            name='Test Resource Model',
            cost_per_unit=10.0,
            no_of_units=5,
            fungible=True,
            type=resource_type
        )

        segment_param = SegmentParam.objects.create(
            code='SP123',
            name='Test Segment Param',
            container=True
        )

        # Define the start and end times for container and lunch segments
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        container_start = today.replace(hour=10)
        container_end = today.replace(hour=22)
        lunch_start = today.replace(hour=15)
        lunch_end = today.replace(hour=16)

        # Create container TimeResourcesQueue instance
        self.container_trq = TimeResourcesQueue.objects.create(
            resource_item_code='RIC123',
            resource_item_name='Container Segment',
            segment_type=1,
            segment='Container',
            segment_start=container_start,
            segment_end=container_end,
            resource_model=resource_model,
            segment_params=segment_param
        )

        # Create lunch TimeResourcesQueue instance
        self.lunch_trq = TimeResourcesQueue.objects.create(
            resource_item_code='RIC124',
            resource_item_name='Lunch Segment',
            segment_type=2,
            segment='Lunch',
            segment_start=lunch_start,
            segment_end=lunch_end,
            resource_model=resource_model,
            segment_params=segment_param
        )

    def test_post_delete_signal(self):
        # Delete the lunch segment
            self.lunch_trq.delete()

            # Check the TimeResourcesQueue table
            remaining_trqs = TimeResourcesQueue.objects.all()
            self.assertEqual(remaining_trqs.count(), 1)
            self.assertEqual(remaining_trqs.first(), self.container_trq)

            # Check the ResourceAvailability table
            availability_segments = ResourceAvailability.objects.filter(resource_item=self.container_trq).order_by('available_start')
            self.assertEqual(availability_segments.count(), 1)

            # Verify the time ranges of the availability segments
            first_availability = availability_segments.first()
            self.assertEqual(first_availability.available_start, self.container_trq.segment_start)
            self.assertEqual(first_availability.available_end, self.container_trq.segment_end)
            
            # Here, additional assertions can be added as needed.