# submit_order.py
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders, OrderItems, ModalCount, Phase, PhaseResource, ResourceType
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

def identify_resources_for_phase(phase):
    # Assuming 'T' is the code for time resources in your ResourceType model
    time_resources_code = 'T'
    resources = PhaseResource.objects.filter(
        phase_code=phase, 
        resource_types_code=time_resources_code
    )
    logger.debug(f"Identified time resources for phase {phase.name}: {[resource.name for resource in resources]}")
    return resources

@api_view(['POST'])
def create_order_and_items(request):
    with transaction.atomic():
        order_data = request.data.get('order')
        order_number = order_data.get('order_number')
        logger.debug("Received order number: %s", order_number)

        order = Orders(
            item_count=order_data['item_count'],
            order_price=order_data['order_price'],
            order_number=order_number
        )

        temp_order_items = []
        for item_data in request.data.get('items', []):
            modal_count_code = item_data.get('modal_count')  # Assuming you're now receiving a code, not an ID
            modal_count = get_object_or_404(ModalCount, code=modal_count_code)  # Fetch using code instead of pk (id)

            order_item = OrderItems(
                order=order,
                modal_count=modal_count,
                item_name=item_data['item_name'],
                unit_price=item_data['unit_price'],
                item_count=item_data['item_count'],
                item_price=item_data['item_price'],
            )
            temp_order_items.append((modal_count.sequence, order_item))

        temp_order_items.sort(key=lambda x: x[0])

        for _, order_item in temp_order_items:
            order_item.save()
            phases = identify_phases_for_order_item(order_item)
            for phase in phases:
                time_resources = identify_resources_for_phase(phase)

        order.save()
        return Response({'status': 'OK', 'order_number': order.order_number})
