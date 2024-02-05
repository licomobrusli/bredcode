from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Orders, OrderItems

class OrderAPITests(TestCase):
    def setUp(self):
        # Set up any pre-requisites for your tests here
        self.client = APIClient()
        
    def test_create_order_and_items(self):
        # Arrange
        url = '/api/submit_order/'  # Use the full path based on your project-level urls.py
        pre_generated_order_number = 'M1170901001XYZ'  # Example pre-generated order number
        order_data = {
            'order': {
                'item_count': 2,
                'order_price': 300,
                'order_number': pre_generated_order_number  # Include the pre-generated order number
            },
            'items': [
                {
                    'item_name': 'Shampoo',
                    'unit_price': 100,
                    'item_count': 2,
                    'item_price': 200
                },
                {
                    'item_name': 'Conditioner',
                    'unit_price': 100,
                    'item_count': 1,
                    'item_price': 100
                }
            ]
        }

        # Act
        response = self.client.post(url, order_data, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'Order and items submitted successfully')
        self.assertIn('order_number', response.data)
        self.assertEqual(response.data['order_number'], pre_generated_order_number)  # Verify that the received order number matches the pre-generated one
        # Verify that the order was created in the database
        self.assertTrue(Orders.objects.filter(order_number=pre_generated_order_number).exists())
        # Verify that the order items were created in the database
        order = Orders.objects.get(order_number=pre_generated_order_number)
        self.assertEqual(order.orderitems_set.count(), len(order_data['items']))
