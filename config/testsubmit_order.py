# testsubmit_order.py
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
        order_data = {
            'order': {
                'item_count': 2,
                'order_price': 300,
                'order_counter': 1
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

        # Print the entire response data
        print("Response data:", response.data)

        # Print the order number from the response
        # This will also confirm if 'order_number' is part of the response
        print("Generated order number:", response.data.get('order_number', 'No order number in response'))

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'Order and items submitted successfully')
        self.assertIn('order_number', response.data)
        # Verify that the order was created in the database
        self.assertTrue(Orders.objects.filter(order_number=response.data['order_number']).exists())
        # Verify that the order items were created in the database
        order = Orders.objects.get(order_number=response.data['order_number'])
        self.assertEqual(order.orderitems_set.count(), len(order_data['items']))
