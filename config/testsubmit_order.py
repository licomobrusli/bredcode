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
            contained=False,
            available=True,
            working=True,
            active=True,
            paid=True,
            calc_pay=0,
            calc_available=0
        )

        # Create Segment instances
        self.segment_shampoo = Segment.objects.create(
            code='SH01',
            type='Product Type',
            segment_param=self.segment_param
        )
        
        self.segment_conditioner = Segment.objects.create(
            code='CO01',
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
        self.modal_count_conditioner = ModalCount.objects.create(
            code=self.segment_conditioner,
            name='Conditioner',
            description='Conditioner Description',
            duration=5,
            price=100.00,
            max_quantity=10,
            category_code=self.service_category,
            service_code=self.service
        )
        
        self.resource_type = ResourceType.objects.create(code='T', name='Time Resource', measure='Unit', unit_size=1)
        self.resource_model = ResourceModel.objects.create(code='RM01', name='Model 1', type=self.resource_type, cost_per_unit=100.00, no_of_units=10, fungible=False)

        container_segment_param = SegmentParam.objects.create(
            code='CTNT',
            name='Container Segment',
            container=True,
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

        # Phases and resources setup for the new test case
        self.phase1 = Phase.objects.create(code='PH01', name='Phase 1', modal_count=self.modal_count_shampoo, sequence=1, duration=10)
        self.phase2 = Phase.objects.create(code='PH02', name='Phase 2', modal_count=self.modal_count_conditioner, sequence=2, duration=15)
        PhaseResource.objects.create(code='PR01', name='Resource 1', phase_code=self.phase1, resource_models_code=self.resource_model, resource_types_code=self.resource_type)
        PhaseResource.objects.create(code='PR02', name='Resource 2', phase_code=self.phase2, resource_models_code=self.resource_model, resource_types_code=self.resource_type)

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
                    'modal_count': self.modal_count_shampoo.code.code,
                    'item_name': 'Shampoo',
                    'unit_price': 100.00,
                    'item_count': 1,
                    'item_price': 100.00
                },
                {
                    'modal_count': self.modal_count_conditioner.code.code,
                    'item_name': 'Conditioner',
                    'unit_price': 100.00,
                    'item_count': 1,
                    'item_price': 100.00
                }
            ]
        }

        # Act
        response = self.client.post(url, order_data, format='json')

        # Verify response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'OK')
        self.assertIn('order_number', response.data)
        self.assertEqual(response.data['order_number'], 'ORD123456')

        # Verify order and items creation
        order_exists = Orders.objects.filter(order_number='ORD123456').exists()
        self.assertTrue(order_exists)
        if order_exists:
            order = Orders.objects.get(order_number='ORD123456')
            self.assertEqual(order.orderitems_set.count(), 2)
            for item_data in order_data['items']:
                self.assertTrue(OrderItems.objects.filter(order=order, item_name=item_data['item_name'], item_price=item_data['item_price']).exists())

            # Assertions for phase and resource allocation
            for item in order.orderitems_set.all():
                phases = Phase.objects.filter(modal_count=item.modal_count).order_by('sequence')
                self.assertGreater(phases.count(), 0, f"Phases should be defined for modal count {item.modal_count}")
                
                for phase in phases:
                    phase_resources = PhaseResource.objects.filter(phase_code=phase)
                    self.assertGreater(phase_resources.count(), 0, f"Resources should be allocated for phase {phase.code}")
                    
                    for phase_resource in phase_resources:
                        trq_exists = TimeResourcesQueue.objects.filter(
                            segment__modal_count=item.modal_count,
                            resource_model=phase_resource.resource_models_code
                        ).exists()
                        self.assertTrue(trq_exists, f"TimeResourcesQueue entry should exist for resource model {phase_resource.resource_models_code.code} and segment {item.modal_count.code}")

        # Verify TimeResourcesQueue creation
        trqs = TimeResourceItems.objects.all()
        self.assertEqual(trqs.count(), 1)
        self.assertTrue(trqs.filter(resource_model=self.resource_model).exists())
        self.assertTrue(trqs.filter(resource_model=self.resource_model).exists())

        # Verify TimeResourcesQueue creation
        trqs = TimeResourcesQueue.objects.all()
        self.assertGreater(trqs.count(), 0, "TimeResourcesQueue entries should be created")
        for trq in trqs:
            self.assertTrue(trq.resource_item_code is not None, "Resource item code should be set")
            self.assertTrue(trq.segment is not None, "Segment should be set")