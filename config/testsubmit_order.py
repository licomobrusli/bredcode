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
        self.phase2 = Phase.objects.create(code='PH02', name='Phase 2', modal_count=self.modal_count_shampoo, sequence=2, duration=15)
        PhaseResource.objects.create(code='PR01', name='Resource 1', phase_code=self.phase1, resource_models_code=self.resource_model, resource_types_code=self.resource_type)
        PhaseResource.objects.create(code='PR02', name='Resource 2', phase_code=self.phase2, resource_models_code=self.resource_model, resource_types_code=self.resource_type)

        # Phases and resources setup for the new test case for conditioner
        self.phase3 = Phase.objects.create(code='PH03', name='Phase 1', modal_count=self.modal_count_conditioner, sequence=1, duration=10)
        self.phase4 = Phase.objects.create(code='PH04', name='Phase 2', modal_count=self.modal_count_conditioner, sequence=2, duration=15)
        PhaseResource.objects.create(code='PR03', name='Resource 1', phase_code=self.phase3, resource_models_code=self.resource_model, resource_types_code=self.resource_type)
        PhaseResource.objects.create(code='PR04', name='Resource 2', phase_code=self.phase4, resource_models_code=self.resource_model, resource_types_code=self.resource_type)

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
                },
                {
                    'modal_count': self.segment_conditioner.code,
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

        # Verify TRQ creation logic
        order = Orders.objects.get(order_number='ORD123456')
        order_items = OrderItems.objects.filter(order=order)
        
        for order_item in order_items:
            # Asserting that phases exist for each order item - this might be a point where TRQ creation fails if missing
            phases = Phase.objects.filter(modal_count=order_item.modal_count)
            self.assertTrue(phases.exists(), f"No phases found for order item {order_item.item_name}")

            for phase in phases:
                # Asserting that resources exist for each phase - another potential failure point
                phase_resources = PhaseResource.objects.filter(phase_code=phase)
                self.assertTrue(phase_resources.exists(), f"No resources found for phase {phase.name} in order item {order_item.item_name}")
                self.assertEqual(phase_resources.count(), 1, f"Expected 1 resource for phase {phase.name} in order item {order_item.item_name}")
                self.assertTrue(phase_resources.filter(resource_models_code=self.resource_model).exists(), f"Resource model not found for phase {phase.name} in order item {order_item.item_name}")
                self.assertTrue(phase_resources.filter(resource_types_code=self.resource_type).exists(), f"Resource type not found for phase {phase.name} in order item {order_item.item_name}")
                self.assertTrue(phase_resources.filter(phase_code=phase).exists(), f"Phase not found for phase {phase.name} in order item {order_item.item_name}")
                self.assertTrue(phase_resources.filter(code__in=[f'PR0{i+1}' for i in range(2)]).exists(), f"Resource not found for phase {phase.name} in order item {order_item.item_name}")

                # Asserting that TRQ entries exist for each phase
                trq_entries = TimeResourcesQueue.objects.filter(segment=phase)
                self.assertTrue(trq_entries.exists(), f"No TRQ entries found for phase {phase.name} in order item {order_item.item_name}")
                self.assertEqual(trq_entries.count(), 1, f"Expected 1 TRQ entry for phase {phase.name} in order item {order_item.item_name}")
                self.assertTrue(trq_entries.filter(resource_item_code=self.timeResourceItem).exists(), f"Resource item not found for phase {phase.name} in order item {order_item.item_name}")
                self.assertTrue(trq_entries.filter(segment=phase).exists(), f"Phase not found for phase {phase.name} in order item {order_item.item_name}")
                self.assertTrue(trq_entries.filter(resource_model=self.resource_model).exists(), f"Resource model not found for phase {phase.name} in order item {order_item.item_name}")
                self.assertTrue(trq_entries.filter(segment_params=self.segment_param).exists(), f"Segment param not found for phase {phase.name} in order item {order_item.item_name}")
                self.assertTrue(trq_entries.filter(segment_start__gte=now().replace(hour=10)).exists(), f"Segment start not found for phase {phase.name} in order item {order_item.item_name}")