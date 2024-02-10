from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ServiceCategory, Services, ModalCount, Orders, OrderItems, Phase, PhaseResource, ResourceType, ResourceModel
from config.submit_order import identify_phases_for_order_item, identify_resources_for_phase


class OrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Set up necessary instances for both tests
        self.service_category = ServiceCategory.objects.create(code='SVC1', name='Hair Care', description='Hair Care Services')
        self.service = Services.objects.create(code='SV01', name='Basic Hair Care', description='Basic hair care services', total_duration=30, price=50.00, service_category=self.service_category)
        
        self.modal_count_shampoo = ModalCount.objects.create(code='SH01', name='Shampoo', description='Shampoo Description', duration=5, price=100.00, max_quantity=10, category_code=self.service_category, service_code=self.service)
        self.modal_count_conditioner = ModalCount.objects.create(code='CO01', name='Conditioner', description='Conditioner Description', duration=5, price=100.00, max_quantity=10, category_code=self.service_category, service_code=self.service)
        
        self.resource_type = ResourceType.objects.create(code='RT01', name='Type 1', measure='Unit', unit_size=1)
        self.resource_model = ResourceModel.objects.create(code='RM01', name='Model 1', type=self.resource_type, cost_per_unit=100.00, no_of_units=10, fungible=True)

        # Phases and resources setup for the new test case
        self.phase1 = Phase.objects.create(code='PH01', name='Phase 1', item_code=self.modal_count_shampoo, sequence=1, duration=10)
        self.phase2 = Phase.objects.create(code='PH02', name='Phase 2', item_code=self.modal_count_conditioner, sequence=2, duration=15)
        PhaseResource.objects.create(code='PR01', name='Resource 1', phase_code=self.phase1, resource_models_code=self.resource_model, resource_types_code=self.resource_type)
        PhaseResource.objects.create(code='PR02', name='Resource 2', phase_code=self.phase2, resource_models_code=self.resource_model, resource_types_code=self.resource_type)

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
                    'modal_count': self.modal_count_shampoo.id,
                    'item_name': 'Shampoo',
                    'unit_price': 100.00,
                    'item_count': 1,
                    'item_price': 100.00
                },
                {
                    'modal_count': self.modal_count_conditioner.id,
                    'item_name': 'Conditioner',
                    'unit_price': 100.00,
                    'item_count': 1,
                    'item_price': 100.00
                }
            ]
        }

        # Act
        response = self.client.post(url, order_data, format='json')

        # Assert
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
