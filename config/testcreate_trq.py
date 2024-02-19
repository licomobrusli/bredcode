from django.test import TestCase
from config.submit_order import create_time_resource_queue_entry
from .models import TimeResourceItems, Segment, ResourceModel, SegmentParam, ResourceType, ResourceAvailability, TimeResourcesQueue
from datetime import timedelta
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)


class TimeResourcesQueueTestCase(TestCase):
    def setUp(self):
        # Create ResourceType instance
        resource_type = ResourceType.objects.create(
            code='T',
            name='Time resource',
            measure='minutes',
            unit_size=1,
        )

        # create ResourceModel instance
        self.resource_model = ResourceModel.objects.create(
            code='BARB',
            name='A barber',
            type=resource_type,
            cost_per_unit=10,
            fungible=False,
            no_of_units=5,
        )

        # Create TimeResourceItems instance
        self.resource_item = TimeResourceItems.objects.create(
            resource_item_code='pmontoya',
            name='Pablo Montoya',
            description='Test Description',
            resource_model=self.resource_model
        )

        # Create a SegmentParam instance for container segment
        self.segment_param_cntn = SegmentParam.objects.create(
            code='CNTN',
            name='Test Container Param',
            description='Description for Test Container Param',
            container=True,
            contained=False,
            available=True,
            working=True,
            active=False,
            paid=True,
            calc_pay=1,
            calc_available=1
        )

        # Use the created SegmentParam instance for the Segment
        self.segment_cntn = Segment.objects.create(
            code='CNTN',
            type='CS',
            segment_param=self.segment_param_cntn
        )

        self.segment_start_cntn = timezone.now() - timedelta(hours=1)
        self.segment_end_cntn = timezone.now() + timedelta(hours=4)

        # Create timeresourcequeue entry for container segment
        create_time_resource_queue_entry(
            resource_item_code=self.resource_item.resource_item_code,
            segment=self.segment_cntn,
            segment_start=self.segment_start_cntn,
            segment_end=self.segment_end_cntn,
            resource_model=self.resource_model,
            segment_params=self.segment_param_cntn
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
        logger.debug(self.resource_item)
        
        # check timeresourcequeue container entry
        self.assertTrue(TimeResourcesQueue.objects.filter(
            resource_item_code=self.resource_item.resource_item_code,
            segment=self.segment_cntn,
            segment_start=self.segment_start_cntn,
            segment_end=self.segment_end_cntn,
            resource_model=self.resource_model
        ).exists(), "TimeResourcesQueue container should exist.")
        
        self.assertEqual(TimeResourcesQueue.objects.count(), 1, "TimeResourcesQueue should have 1 before after adding 2nd.")
        
        # Now, check if ResourceAvailability has been updated correctly.
        availability_before = ResourceAvailability.objects.count()
        self.assertEqual(availability_before, 1, "ResourceAvailability should be singular before creating TimeResourcesQueue entry.")

        # Call the function to create a new TimeResourcesQueue entry
        create_time_resource_queue_entry(
            resource_item_code=self.resource_item.resource_item_code,
            segment=self.segment,
            segment_start=self.segment_start,
            segment_end=self.segment_end,
            resource_model=self.resource_model,
            segment_params=self.segment_param
        )

        # check timeresourcequeue entry
        self.assertTrue(TimeResourcesQueue.objects.filter(
            resource_item_code=self.resource_item.resource_item_code,
            segment=self.segment,
            segment_start=self.segment_start,
            segment_end=self.segment_end,
            resource_model=self.resource_model
        ).exists(), "TimeResourcesQueue entry should exist after creating it.")

        self.assertEqual(TimeResourcesQueue.objects.count(), 2, "TimeResourcesQueue should have 2 entries after adding 2nd.")
        
        TRQ = TimeResourcesQueue.objects.filter()
        logger.debug(TRQ)

        # Now, check if ResourceAvailability has been updated correctly.
        availability_after = ResourceAvailability.objects.count()
        self.assertEqual(availability_after, 2, "ResourceAvailability should be updated after creating TimeResourcesQueue entry.")

        RA = ResourceAvailability.objects.filter()
        logger.debug(RA)