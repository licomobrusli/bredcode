# submit_order.py
from django.db import transaction, models
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from django.db.models.functions import Coalesce
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders, OrderItems, ModalCount, Phase, PhaseResource, ResourceType, ResourceAvailability, TimeResourcesQueue, Segment, SegmentParam, SimpleModel
import logging
from django.utils import timezone
import sys

logger = logging.getLogger(__name__)

def identify_phases_for_order_item(order_item):
    phases = Phase.objects.filter(modal_count=order_item.modal_count).order_by('sequence')
    logger.debug(f"Identified phases for item {order_item.item_name}: {[phase.name for phase in phases]}")
    return phases

def identify_resources_for_phase(phase):
    # Assuming 'T' is the code for time resources in your ResourceType model
    time_resources_code = 'T'
    resources = PhaseResource.objects.filter(
        phase_code=phase, 
        resource_types_code__code=time_resources_code
    )
    logger.debug(f"Identified time resources for phase {phase.name}: {[resource.resource_models_code.name for resource in resources]}")
    return resources


def find_earliest_availability(resource_model_code, phase_duration, last_phase_end_time=None):
    initial_start_time = now().replace(microsecond=0)
    if last_phase_end_time:
        initial_start_time = max(initial_start_time, last_phase_end_time)

    # Adjust the filter conditions based on the corrected logic
    conditions = Q(
        available_start__lt=initial_start_time,
        available_end__gte=initial_start_time + timedelta(minutes=phase_duration)
    ) | Q(
        available_start__gte=initial_start_time,
        available_end__gte=F('available_start') + timedelta(minutes=phase_duration)
    )

    # Apply the corrected conditions
    availability = ResourceAvailability.objects.filter(
        conditions,
        resource_model=resource_model_code
    ).order_by('available_start').first()

    if availability:
        actual_start_time = max(availability.available_start, initial_start_time)
        return actual_start_time, actual_start_time + timedelta(minutes=phase_duration), availability.resource_item
    
    return None, None, None

def create_time_resource_queue_entry(resource_item_code, segment, segment_start, segment_end, resource_model, segment_params=None):
    print(f"Creating new queue entry for resource item: {resource_item_code}, segment: {segment}, start: {segment_start}, end: {segment_end}, resource model: {resource_model}")
    new_queue_entry = TimeResourcesQueue(
        resource_item_code=resource_item_code,
        segment=segment,
        segment_start=segment_start,
        segment_end=segment_end,
        resource_model=resource_model,
        segment_params=segment_params,
    )

    # Save the new queue entry
    print(f"Saving new queue entry: {new_queue_entry}")
    new_queue_entry.save()

    # Return the new entry
    return new_queue_entry

# write a function to #create entry in simple_model.code = 1
def create_entry_in_simple_model():
    simple_model = SimpleModel.objects.create(
        code='1',
    )
    return simple_model

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
        order.save()

        temp_order_items = []
        for item_data in request.data.get('items', []):
            modal_count_code = item_data.get('modal_count')
            modal_count = get_object_or_404(ModalCount, code=modal_count_code)

            order_item = OrderItems(
                order=order,
                modal_count=modal_count,
                item_name=item_data['item_name'],
                unit_price=item_data['unit_price'],
                item_count=item_data['item_count'],
                item_price=item_data['item_price'],
            )   
            order_item.save()
            # create_entry_in_simple_model()
            temp_order_items.append((modal_count.sequence, order_item))

        temp_order_items.sort(key=lambda x: x[0])
        
        for _, order_item in temp_order_items:
            phases = identify_phases_for_order_item(order_item)
            last_phase_end_time = None
            # create_entry_in_simple_model()
            for phase in phases:
                segment = phase.modal_count.code
                time_resources = identify_resources_for_phase(phase)
                for resource in time_resources:
                    start_time, end_time, resource_item = find_earliest_availability(resource.resource_models_code.code, phase.duration, last_phase_end_time)
                    if start_time and end_time and resource_item:
                        # create_entry_in_simple_model()
                        new_queue_entry = create_time_resource_queue_entry(
                            resource_item_code=resource_item,
                            segment=segment,
                            segment_start=start_time,
                            segment_end=end_time,
                            resource_model=resource.resource_models_code,
                            segment_params=None
                        )
                        last_phase_end_time = end_time
                        break
                    else:
                        logger.error(f"No available resource found for phase {phase.name} of item {order_item.item_name}")

        return Response({'status': 'OK', 'order_number': order.order_number})
