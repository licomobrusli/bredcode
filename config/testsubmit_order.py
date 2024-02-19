# testsubmit_order.py
from datetime import timedelta
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ServiceCategory, Services, ModalCount, Orders, OrderItems, Phase, PhaseResource, ResourceType, ResourceModel, Segment, SegmentParam, ResourceAvailability, TimeResourceItems, TimeResourcesQueue
from django.utils.timezone import now


class OrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
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
            calc_available=-1
        )

        # Create Segment instances
        self.segment_shampoo = Segment.objects.create(
            code='SH01',
            type='Product Type',
            segment_param=self.segment_param
        )
        
        # Set up necessary instances for both tests
        self.service_category = ServiceCategory.objects.create(code='SVC1', name='Hair Care', description='Hair Care Services')
        self.service = Services.objects.create(code='SV01', name='Basic Hair Care', description='Basic hair care services', total_duration=30, price=50.00, service_category=self.service_category)
        
        self.modal_count_shampoo = ModalCount.objects.create(
            code=self.segment_shampoo,
            name='Shampoo',
            description='Shampoo Description',
            duration=5,
            price=100.00,
            max_quantity=10,
            category_code=self.service_category,
            service_code=self.service
        )
        
        self.resource_type = ResourceType.objects.create(code='T', name='Time Resource', measure='Unit', unit_size=1)
        self.resource_model = ResourceModel.objects.create(code='RM01', name='Model 1', type=self.resource_type, cost_per_unit=100.00, no_of_units=10, fungible=False)

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
        
        segment_instance = Segment.objects.create(
            code='SHFT',
            type='SC',
            segment_param=container_segment_param
        )
        
        today = now().replace(hour=0, minute=0, second=0, microsecond=0)
        container_start = today.replace(hour=10)
        container_end = today.replace(hour=22)

        # Phases and resources setup for the new test case for shampoo
        self.phase1 = Phase.objects.create(code='PH01', name='Phase 1', modal_count=self.modal_count_shampoo, sequence=1, duration=10)
        PhaseResource.objects.create(code='PR01', name='Resource 1', phase_code=self.phase1, resource_models_code=self.resource_model, resource_types_code=self.resource_type)
        
        self.timeResourceItem = TimeResourceItems.objects.create(
            resource_item_code='TRI001',
            name='Test Resource Item',
            description='A test resource item for availability',
            start_date=now().date(),
            resource_model=self.resource_model
        )

        self.container_trq = TimeResourcesQueue.objects.create(
            resource_item_code=self.timeResourceItem,
            segment=segment_instance,
            segment_start=container_start,
            segment_end=container_end,
            resource_model=self.resource_model,
            segment_params=container_segment_param
        )


    def test_create_order_and_order_items(self):
        # Arrange
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
                    'unit_price': 100.00,
                    'item_count': 1,
                    'item_price': 100.00
                }
            ]
        }

        # Act
        response = self.client.post(url, order_data, format='json')

        # more assertions
        self.assertEqual(self.modal_count_shampoo.code, self.segment_shampoo, "Shampoo ModalCount not correctly linked to Segment.")
        self.assertEqual(self.phase1.modal_count, self.modal_count_shampoo, "Phase 1 not correctly linked to Shampoo ModalCount.")

        # Verify ModalCount and Phase association
        shampoo_phases = Phase.objects.filter(modal_count=self.modal_count_shampoo)
        self.assertTrue(shampoo_phases.exists(), "No phases found for Shampoo ModalCount")
        self.assertTrue(shampoo_phases.filter(id=self.phase1.id).exists(), "Phase1 not linked with Shampoo ModalCount")

        # check resource availability
        self.assertTrue(ResourceAvailability.objects.filter(resource_model=self.resource_model).exists(), "Resource availability not found")
        self.assertEqual(ResourceAvailability.objects.filter(resource_item=self.timeResourceItem).count(), 2, "Resource item availability not found")

        # Verify TRQ entries after submitting the order
        order = Orders.objects.get(order_number='ORD123456')