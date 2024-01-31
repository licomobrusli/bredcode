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

        # Define a common resource item code for the related segments
        common_resource_item_code = 'RIC123'

        # Create container TimeResourcesQueue instance
        self.container_trq = TimeResourcesQueue.objects.create(
            resource_item_code=common_resource_item_code,
            segment='Container',
            segment_start=container_start,
            segment_end=container_end,
            resource_model=resource_model,
            segment_params=segment_param
        )

        # Create lunch TimeResourcesQueue instance
        self.lunch_trq = TimeResourcesQueue.objects.create(
            resource_item_code=common_resource_item_code,
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
            
    def test_post_save_signal(self):
        # Create a new TimeResourcesQueue instance (a meeting, for instance)
        meeting_start = self.container_trq.segment_start + timedelta(hours=1)
        meeting_end = meeting_start + timedelta(hours=2)
        
        # Create the meeting TimeResourcesQueue instance
        # Ensure to use the correct field names as per your model definition
        meeting_trq = TimeResourcesQueue.objects.create(
            resource_item_code=self.container_trq.resource_item_code,  # Use the same resource_item_code
            segment='Meeting',
            segment_start=meeting_start,
            segment_end=meeting_end,
            resource_model=self.container_trq.resource_model,
            segment_params=self.container_trq.segment_params
        )

        # Check the TimeResourcesQueue table
        trqs = TimeResourcesQueue.objects.all()
        self.assertEqual(trqs.count(), 3)  # Container, Lunch, and Meeting

        # Check the ResourceAvailability table
        availability_segments = ResourceAvailability.objects.filter(resource_item=self.container_trq).order_by('available_start')
        self.assertEqual(availability_segments.count(), 2)  # The container availability is now split by the meeting

        # Verify the time ranges of the availability segments
        first_availability, second_availability = availability_segments
        self.assertEqual(first_availability.available_start, self.container_trq.segment_start)
        self.assertEqual(first_availability.available_end, meeting_start)
        self.assertEqual(second_availability.available_start, meeting_end)
        self.assertEqual(second_availability.available_end, self.container_trq.segment_end)

        # Here, additional assertions can be added as needed.
