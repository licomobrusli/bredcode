# submit_order.py
import random, string
from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders, OrderItems

@api_view(['POST'])
def create_order_and_items(request):
    with transaction.atomic():
        # Create an order instance in memory
        order_data = request.data.get('order')
        order_counter = order_data.get('order_counter')

        # Generate the order number using the order_counter
        now = timezone.now()
        franchise_code = 'M1'
        date_str = now.strftime('%y%m%d%H')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        order_number = f"{franchise_code}{date_str}{str(order_counter).zfill(6)}{random_str}"

        print("Franchise code:", franchise_code)
        print("Date string:", date_str)
        print("Order counter:", order_counter)
        print("Random string:", random_str)
        print("Generated order number:", order_number)
        
        # Create an order instance in memory with the generated order_number
        order = Orders(
            item_count=order_data['item_count'],
            order_price=order_data['order_price'],
            order_number=order_number
        )

        # Process order items
        for item_data in request.data.get('items', []):
            OrderItems.objects.create(
                order=order,  # associate with the in-memory order instance
                item_name=item_data['item_name'],
                unit_price=item_data['unit_price'],
                item_count=item_data['item_count'],
                item_price=item_data['item_price'],
            )
        
        # Save the order (which also saves associated order items)
        order.save()

        print("Order number after saving:", order.order_number)
        
        # Return a success response
        return Response({'status': 'Order and items submitted successfully', 'order_number': order.order_number})
