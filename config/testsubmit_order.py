# testsubmit_order.py
from datetime import timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ServiceCategory, Services, ModalCount, Orders, OrderItems, Phase, PhaseResource, ResourceType, ResourceModel, Segment, SegmentParam, ResourceAvailability, TimeResourceItems, TimeResourcesQueue
from django.utils.timezone import now

import logging
logger = logging.getLogger(__name__)

class OrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        container_segment_param = SegmentParam.objects.create(
            code='CNTN',
            name='Container Segment',
            description='A test container segment',
            container=True,
            contained=False,
            available=True,
            working=True,
            active=False,
            paid=True,
            calc_pay=1,
            calc_available=1
        )

        segment_cntn = Segment.objects.create(
            code='SHFT',
            type='SC',
            segment_param=container_segment_param
        )

        self.resource_type = ResourceType.objects.create(
            code='T', 
            name='Time', 
            measure='minute', 
            unit_size=1
        )
        
        self.resource_model = ResourceModel.objects.create(
            code='BARB', 
            name='A barber', 
            type=self.resource_type, # .code mybe?
            cost_per_unit=10, 
            no_of_units=10, 
            fungible=False
        )

        self.timeResourceItem = TimeResourceItems.objects.create(
            resource_item_code='pmontoya',
            name='Pablo Montoya',
            description='A test resource item for availability',
            resource_model=self.resource_model
        )

        today = now().replace(microsecond=0)
        container_start = now() - timedelta(hours=1)
        container_end = now() + timedelta(hours=4)

        self.container_trq = TimeResourcesQueue.objects.create(
            resource_item_code=self.timeResourceItem,
            segment=segment_cntn,
            segment_start=container_start,
            segment_end=container_end,
            resource_model=self.resource_model,
            segment_params=container_segment_param
        )

        self.segment_param = SegmentParam.objects.create(
            code='SP01',
            name='Segment Param 1',
            description='A test segment param',
            container=False,
            contained=True,
            available=False,
            working=True,
            active=True,
            paid=True,
            calc_pay=0,
            calc_available='-1'
        )

        # Create Segment instance
        self.segment_shampoo = Segment.objects.create(
            code='SH01',
            type='Product Type',
            segment_param=self.segment_param
        )
        
        # Set up necessary instances for both tests
        self.service_category = ServiceCategory.objects.create(
            code='SVC1', 
            name='Hair Care', 
            description='Hair Care Services'
        )
        
        self.service = Services.objects.create(
            code='SV01', 
            name='Basic Hair Care', 
            description='Basic hair care services', 
            total_duration=3, 
            price=50, 
            service_category=self.service_category
        )
        
        self.modal_count_shampoo = ModalCount.objects.create(
            code=self.segment_shampoo,
            name='Shampoo',
            description='Shampoo Description',
            duration=3,
            price=10,
            max_quantity=10,
            category_code=self.service_category,
            service_code=self.service,
            logic='NOT',
            sub=0,
            sequence=1,
        )        

        # Phases and resources setup for the new test case for shampoo
        self.phase1 = Phase.objects.create(
            code='PH01', 
            name='Phase 1', 
            sequence=1, 
            duration=3,
            modal_count=self.modal_count_shampoo, 
        )
        
        PhaseResource.objects.create(
            code='PR01', 
            name='Resource 1', 
            phase_code=self.phase1, 
            resource_models_code=self.resource_model, 
            resource_types_code=self.resource_type
        )

    def test_create_order_and_order_items(self):
        # Arrange
        logger.debug(f"Before: {TimeResourcesQueue.objects.all()}")
        logger.debug(f"Before: {ResourceAvailability.objects.all()}")
        url = '/api/submit_order/'
        order_data = {
            'order': {
                'item_count': 2,
                'order_price': 200.00,
                'order_number': 'ORD123456'
            },
            'items': [
                {
                    'modal_count': self.segment_shampoo.code,
                    'item_name': 'Shampoo',
                    'unit_price': 10,
                    'item_count': 1,
                    'item_price': 10,
                }
            ]
        }

        # Act
        logger.debug("Hello World")
        response = self.client.post(url, order_data, format='json')
        logger.debug(f"Response: {response.data}")

        # check resource availability
        logger.debug(f"After: {TimeResourcesQueue.objects.all()}")
        logger.debug(f"After: {ResourceAvailability.objects.all()}")
        
        self.assertTrue(ResourceAvailability.objects.filter(resource_model=self.resource_model).exists(), "Resource availability not found")
        self.assertEqual(ResourceAvailability.objects.filter(resource_item=self.timeResourceItem).count(), 2, "Should be 2 ResourceAvailability entries for same resource item.")

        # check timeresourcequeue entry
        #lgo time resource queue details of all items
        logger.debug(TimeResourcesQueue.objects.all())
        self.assertEqual(TimeResourcesQueue.objects.count(), 2, "TimeResourcesQueue entry should exist after creating it.")

        # Verify TRQ entries after submitting the order
        order = Orders.objects.get(order_number='ORD123456')
        order_items = OrderItems.objects.filter(order=order)
        self.assertEqual(order_items.count(), 1, "Order Items should be 1")