# submit_order.py
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders, OrderItems, ModalCount, Phase, PhaseResource, ResourceAvailability, TimeResourcesQueue
from django.utils.timezone import now
from rest_framework import status
from config.time_utils import now_minutes

import logging

logger = logging.getLogger(__name__)

def identify_phases_for_order_item(order_item):
    phases = Phase.objects.filter(modal_count=order_item.modal_count).order_by('sequence')
    return phases

def identify_resources_for_phase(phase):
    # Assuming 'T' is the code for time resources in your ResourceType model
    time_resources_code = 'T'
    resources = PhaseResource.objects.filter(
        phase_code=phase, 
        resource_types_code__code=time_resources_code
    )
    return resources


def find_earliest_availability(resource_model_code, phase_duration, preferred_resource_items, last_phase_end_time=None):
    initial_start_time = now_minutes().replace(microsecond=0)
    if last_phase_end_time:
        initial_start_time = max(initial_start_time, last_phase_end_time)

    # Define the general conditions for availability.
    general_conditions = Q(
        available_start__lt=initial_start_time,
        available_end__gte=initial_start_time + timedelta(minutes=phase_duration)
    ) | Q(
        available_start__gte=initial_start_time,
        available_end__gte=F('available_start') + timedelta(minutes=phase_duration)
    )

    # Get all available resources.
    all_availabilities = ResourceAvailability.objects.filter(
        general_conditions,
        resource_model=resource_model_code
    )

    # Sort the availabilities first by preference (if they are in the preferred list) and then by available start.
    sorted_availabilities = sorted(all_availabilities, key=lambda x: (
        preferred_resource_items.index(x.resource_item) if x.resource_item in preferred_resource_items else float('inf'),
        x.available_start
    ))

    # Return the first availability that fits the conditions.
    for availability in sorted_availabilities:
        actual_start_time = max(availability.available_start, initial_start_time)
        return actual_start_time, actual_start_time + timedelta(minutes=phase_duration), availability.resource_item

    return None, None, None

def create_time_resource_queue_entry(resource_item_code, segment, segment_start, segment_end, resource_model, segment_params=None, order=None):
    # log what is recieved in full
    logger.debug(f"create_time_resource_queue_entry: {resource_item_code}, {segment}, {segment_start}, {segment_end}, {resource_model}, {segment_params}, {order}")
    new_queue_entry = TimeResourcesQueue(
        resource_item_code=resource_item_code,  # Assign the instance instead of the string
        segment=segment,
        segment_start=segment_start,
        segment_end=segment_end,
        resource_model=resource_model,
        segment_params=segment_params,
        order_number=order,
    )
    new_queue_entry.save()
    return new_queue_entry


@api_view(['POST'])
def create_order_and_items(request):
    with transaction.atomic():
        logger.debug('CREATE_ORDER_AND_ITEMS ##########################################')
        preferred_resource_items = []
        last_phase_end_time = None

        order_data = request.data.get('order')
        order_number = order_data.get('order_number')
        logging.debug(f'Received order data: {order_data}')

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
            logging.debug(f'Processing order item: {item_data}')

            order_item = OrderItems(
                order=order,
                modal_count=modal_count,
                item_name=item_data['item_name'],
                unit_price=item_data['unit_price'],
                item_count=item_data['item_count'],
                item_price=item_data['item_price'],
            )   
            order_item.save()
            temp_order_items.append(order_item)

        # temp_order_items.sort(key=lambda x: x[0])
        logger.debug(f"Temp Order Items: {temp_order_items}")

        for order_item in temp_order_items:
            phases = identify_phases_for_order_item(order_item)
            logger.debug(f"Phases: {phases}")
            for phase in phases:
                time_resources = identify_resources_for_phase(phase)
                logger.debug(f"Time Resources: {time_resources}")
                for resource in time_resources:
                    segment = resource.code
                    start_time, end_time, resource_item = find_earliest_availability(
                        resource.resource_models_code.code,
                        phase.duration,
                        preferred_resource_items,
                        last_phase_end_time
                    )
                    if start_time and end_time and resource_item:
                        logger.debug(f"resource_item: {resource_item}, Segment: {segment}, Start: {start_time}, End: {end_time}, Resource Model: {resource.resource_models_code}, Segment Params: {segment.segment_param}, Order: {order}")
                        create_time_resource_queue_entry(
                            resource_item_code=resource_item,
                            segment=segment,
                            segment_start=start_time,
                            segment_end=end_time,
                            resource_model=resource.resource_models_code,
                            segment_params=segment.segment_param,
                            order=order,
                        )
                        last_phase_end_time = end_time
                        if resource_item not in preferred_resource_items:
                            preferred_resource_items.append(resource_item)
                            logging.debug(f'Added time resource queue entry for resource item {resource_item}')
                        break
                    else:
                        logging.error(f"No available resources for phase {phase}")
                        raise Exception(f"No available resources for phase")
        logging.debug(f'Order processing completed: {order.order_number}')
        return Response({'status': 'OK', 'order_number': order.order_number}, status=status.HTTP_201_CREATED)
