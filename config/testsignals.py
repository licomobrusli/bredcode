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

        # Create SegmentParam instances and assign them to instance variables
        self.container_segment_param = SegmentParam.objects.create(
            code='CSP12',
            name='Container Segment',
            container=True,
            calc_available=1
        )
        self.non_container_segment_param = SegmentParam.objects.create(
            code='NCSP1',
            name='Non-Container Segment',
            container=False,
            calc_available=-1
        )

        # Define the start and end times for container and lunch segments
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        container_start = today.replace(hour=10)
        container_end = today.replace(hour=22)

        # Define a common resource item code for the related segments
        self.common_resource_item_code = 'RIC123'

         # Create container TimeResourcesQueue instance using container_segment_param
        self.container_trq = TimeResourcesQueue.objects.create(
            resource_item_code=self.common_resource_item_code,
            segment='Container',
            segment_start=container_start,
            segment_end=container_end,
            resource_model=resource_model,
            segment_params=self.container_segment_param
        )

    def test_post_delete_signal(self):
        # Check the initial state before adding lunch
        remaining_trqs = TimeResourcesQueue.objects.all()
        self.assertEqual(remaining_trqs.count(), 1)
        self.assertEqual(remaining_trqs.first(), self.container_trq)

        availability_segments = ResourceAvailability.objects.filter(resource_item=self.common_resource_item_code).order_by('available_start')
        self.assertEqual(availability_segments.count(), 1)

        # Create lunch TimeResourcesQueue instance using non_container_segment_param
        lunch_start = timezone.now().replace(hour=15)
        lunch_end = timezone.now().replace(hour=16)
        lunch_trq = TimeResourcesQueue.objects.create(
            resource_item_code=self.common_resource_item_code,
            segment='Lunch',
            segment_start=lunch_start,
            segment_end=lunch_end,
            resource_model=self.container_trq.resource_model,
            segment_params=self.non_container_segment_param
        )

        # Check the state after adding lunch
        remaining_trqs = TimeResourcesQueue.objects.all()
        self.assertEqual(remaining_trqs.count(), 2)

        availability_segments = ResourceAvailability.objects.filter(resource_item=self.common_resource_item_code).order_by('available_start')
        self.assertEqual(availability_segments.count(), 2)

        # Delete the lunch segment
        lunch_trq.delete()

        # Check the state after deleting lunch
        remaining_trqs = TimeResourcesQueue.objects.all()
        self.assertEqual(remaining_trqs.count(), 1)

        availability_segments = ResourceAvailability.objects.filter(resource_item=self.common_resource_item_code).order_by('available_start')
        self.assertEqual(availability_segments.count(), 1)

        # Verify the time ranges of the availability segments
        first_availability = availability_segments.first()
        self.assertEqual(first_availability.available_start, self.container_trq.segment_start)
        self.assertEqual(first_availability.available_end, self.container_trq.segment_end)
