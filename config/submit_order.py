# submit_order.py
from django.db import transaction, models
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Orders, OrderItems, ModalCount, Phase, PhaseResource, ResourceType, ResourceAvailability, TimeResourcesQueue, Segment, SegmentParam
import logging

logger = logging.getLogger(__name__)

def identify_phases_for_order_item(order_item):
    phases = Phase.objects.filter(item_code=order_item.modal_count).order_by('sequence')
    logger.debug(f"Identified phases for item {order_item.item_name}: {[phase.name for phase in phases]}")
    return phases

def identify_resources_for_phase(phase):
    # Assuming 'T' is the code for time resources in your ResourceType model
    time_resources_code = 'T'
    resources = PhaseResource.objects.filter(
        phase_code=phase, 
        resource_types_code=time_resources_code
    )
    logger.debug(f"Identified time resources for phase {phase.name}: {[resource.resource_models_code.name for resource in resources]}")
    return resources


def find_earliest_availability(resource_model_code, phase_duration, last_phase_end_time=None):
    initial_start_time = now() if last_phase_end_time is None else max(now(), last_phase_end_time)

    availability = ResourceAvailability.objects.annotate(
        live_start=models.functions.Coalesce(
            models.Case(
                models.When(available_start__gte=initial_start_time, then='available_start'),
                default=models.Value(initial_start_time)
            ),
            output_field=models.DateTimeField()
        ),
        live_end=models.ExpressionWrapper(
            models.F('live_start') + timedelta(minutes=phase_duration),
            output_field=models.DateTimeField()
        )
    ).filter(
        resource_model=resource_model_code,
        available_end__gte=models.F('live_end')
    ).order_by('available_start').first()
    
    if availability:
        # No need for additional checks, as the availability has already been confirmed
        return availability.live_start, availability.live_start + timedelta(minutes=phase_duration), availability.resource_item

    # If no suitable availability is found, return None
    return None, None, None

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
            temp_order_items.append((modal_count.sequence, order_item))

        temp_order_items.sort(key=lambda x: x[0])

        for _, order_item in temp_order_items:
            phases = identify_phases_for_order_item(order_item)
            last_phase_end_time = None
            for phase in phases:
                time_resources = identify_resources_for_phase(phase)
                for resource in time_resources:
                    start_time, end_time, resource_item = find_earliest_availability(resource.resource_models_code.code, phase.duration, last_phase_end_time)
                    if start_time and end_time and resource_item:
                        segment = Segment.objects.filter(modal_count=order_item.modal_count).first()
                        if not segment:
                            logger.error("No segment found for the modal count: %s", order_item.modal_count.code)
                            continue
                        
                        TimeResourcesQueue.objects.create(
                            resource_item_code=resource_item,
                            segment=segment,
                            segment_start=start_time,
                            segment_end=end_time,
                            resource_model=resource.resource_models_code,
                            segment_params=segment.segment_param
                        )
                        last_phase_end_time = end_time
                    else:
                        logger.error("No availability found for resource: %s, phase: %s", resource.name, phase.name)
                                # Handle no availability scenario, e.g., break or return an error response

        return Response({'status': 'OK', 'order_number': order.order_number})