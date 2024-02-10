# submit_order.py
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders, OrderItems, Phase, PhaseResource
import logging

logger = logging.getLogger(__name__)

def identify_phases_for_order_item(order_item):
    phases = Phase.objects.filter(item_code=order_item.modal_count).order_by('sequence')
    logger.debug(f"Identified phases for item {order_item.item_name}: {[phase.name for phase in phases]}")
    return phases

def identify_resources_for_phase(phase):
    resources = PhaseResource.objects.filter(phase_code=phase)
    logger.debug(f"Identified resources for phase {phase.name}: {[resource.name for resource in resources]}")
    return resources

@api_view(['POST'])
def create_order_and_items(request):
    with transaction.atomic():
        # Extract the order data from the request
        order_data = request.data.get('order')
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
            order_item = OrderItems.objects.create(
                order=order,  # associate with the in-memory order instance
                modal_count=item_data['modal_count'],
                item_name=item_data['item_name'],
                unit_price=item_data['unit_price'],
                item_count=item_data['item_count'],
                item_price=item_data['item_price'],
            )
            # Immediately after creating an order item, identify its phases
            phases = identify_phases_for_order_item(order_item)
            for phase in phases:
                # Identify resources for each phase and log them
                resources = identify_resources_for_phase(phase)
                # You can use these resources as needed in your application logic

        # Save the order (which also saves associated order items)
        order.save()

        # Return a success response
        return Response({'status': 'OK', 'order_number': order.order_number})
