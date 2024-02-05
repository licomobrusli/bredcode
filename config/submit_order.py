# submit_order.py
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders, OrderItems
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def create_order_and_items(request):
    with transaction.atomic():
        # Extract the order data from the request
        order_data = request.data.get('order')

        # Use the pre-generated order number from the request
        order_number = order_data.get('order_number')
        logger.debug("Received order number: %s", order_number)

        # Create an order instance in memory with the received order_number
        order = Orders(
            item_count=order_data['item_count'],
            order_price=order_data['order_price'],
            order_number=order_number  # Use the received order number
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

        # Return a success response
        return Response({'status': 'Order and items submitted successfully', 'order_number': order.order_number})
