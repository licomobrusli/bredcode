from django.test import TestCase
from config.submit_order import create_time_resource_queue_entry
from .models import TimeResourceItems, Segment, ResourceModel, SegmentParam, TimeResourcesQueue, ResourceType
from datetime import datetime, timedelta
from django.utils import timezone

class TimeResourcesQueueTestCase(TestCase):
    def setUp(self):
        # Create or fetch a ResourceType instance
        resource_type, created = ResourceType.objects.get_or_create(
            code='RT123',  # Use appropriate code for your ResourceType
            defaults={
                'name': 'Test Resource Type',
                'measure': 'Unit',  # Adjust this field based on your model
                'unit_size': 1,  # Adjust this field based on your model
            }
        )

        # Now, use the created or fetched ResourceType instance for the ResourceModel
        self.resource_model = ResourceModel.objects.create(
            code='RM123',
            name='Test Resource Model',
            type=resource_type,  # Use the created or fetched ResourceType instance here
            cost_per_unit=100,  # Adjust these fields based on your model
            no_of_units=5,  # Adjust these fields based on your model
        )

        # The rest of your setup continues as before...
        self.resource_item = TimeResourceItems.objects.create(
            resource_item_code='RI12345',
            name='Test Resource Item',
            description='Test Description',
            start_date=timezone.now().date(),
            resource_model=self.resource_model
        )


        # Create a SegmentParam instance before creating a Segment instance
        self.segment_param = SegmentParam.objects.create(
            code='SP123',
            name='Test Segment Param',
            description='Description for Test Segment Param',
            container=False,
            contained=True,
            available=False,
            working=True,
            active=True,
            paid=True,
            calc_pay=0,
            calc_available=-1
        )

        # Use the created SegmentParam instance for the Segment
        self.segment = Segment.objects.create(
            code='SG123',
            type='Test Segment',
            segment_param=self.segment_param
        )

        self.segment_start = timezone.now()
        self.segment_end = timezone.now() + timedelta(hours=1)

    def test_create_time_resource_queue_entry(self):
        # Call the function to create a new TimeResourcesQueue entry
        new_entry = create_time_resource_queue_entry(
            resource_item_code=self.resource_item,
            segment=self.segment,
            segment_start=self.segment_start,
            segment_end=self.segment_end,
            resource_model=self.resource_model,
            segment_params=None  # Adjust based on your model's needs or provide valid parameters
        )

        # Check that the entry was created and contains the correct information
        self.assertIsNotNone(new_entry.id, "The new TimeResourcesQueue entry should have an ID.")
        self.assertEqual(new_entry.segment, self.segment, "The segment should match the one provided.")
        self.assertEqual(new_entry.resource_item_code, self.resource_item, "The resource item code should match the one provided.")
        self.assertEqual(new_entry.segment_start, self.segment_start, "The segment start time should match the one provided.")
        self.assertEqual(new_entry.segment_end, self.segment_end, "The segment end time should match the one provided.")
        self.assertEqual(new_entry.resource_model, self.resource_model, "The resource model should match the one provided.")
