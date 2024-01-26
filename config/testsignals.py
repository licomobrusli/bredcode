# tests.py
from django.test import TestCase
from .models import TimeResourcesQueue, ResourceModel, SegmentParam, ResourceType
from django.utils import timezone

class TimeResourcesQueueSignalTest(TestCase):
    def setUp(self):
        # Create a ResourceType instance first
        resource_type = ResourceType.objects.create(
            code='T',  # Use a code that matches type_id in ResourceModel
            name='Test Resource Type',
            measure='Unit',
            unit_size=1
        )

        # Now create ResourceModel instance with the created ResourceType
        resource_model = ResourceModel.objects.create(
            code='RM123',
            name='Test Resource Model',
            cost_per_unit=10.0,
            no_of_units=5,
            fungible=True,
            type=resource_type  # Assign the created ResourceType instance here
        )

        segment_param = SegmentParam.objects.create(
            code='SP123',
            name='Test Segment Param',
            container=True
        )

        # Create a TimeResourcesQueue instance
        # Note: Use timezone.now() directly for DateTimeFields
        self.trq_instance = TimeResourcesQueue.objects.create(
            resource_item_code='RIC123',
            resource_item_name='Test Resource Item',
            segment_type=1,
            segment='Test Segment',
            segment_start=timezone.now(),
            segment_end=timezone.now(),
            resource_model=resource_model,
            segment_params=segment_param
        )

    def test_post_delete_signal(self):
        # Store the count before deletion
        initial_count = TimeResourcesQueue.objects.count()

        # Delete the instance
        self.trq_instance.delete()

        # Check if the count has decreased by 1
        self.assertEqual(TimeResourcesQueue.objects.count(), initial_count - 1)

        # Here you can add more assertions to verify that the signal did what it's supposed to do.
