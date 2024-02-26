from rest_framework import serializers
from config.models import Services, ServiceCategory, ModalCount, ModalSelect, Orders, OrderItems, TimeResourcesQueue
import logging

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'code', 'name', 'description', 'image_path', 'date_created']

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id', 'code', 'name', 'description', 'price', 'total_duration', 'image_path', 'service_category', 'date_created']

class ModalCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModalCount
        fields = ['code', 'name', 'description', 'duration', 'price', 'max_quantity', 'category_code', 'service_code', 'image_path', 'date_created', 'logic', 'sub']

class ModalSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModalSelect
        fields = ['id', 'code', 'name', 'description', 'duration', 'price', 'category_code', 'service_code', 'image_path', 'date_created']

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'item_count', 'order_price', 'est_start', 'est_duration', 'start', 'duration', 'time_created', 'date_created', 'order_number']
        read_only_fields = ['id', 'time_created', 'date_created']

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id', 'order', 'modal_count', 'item_name', 'unit_price', 'item_count', 'item_price', 'est_start', 'est_duration', 'start', 'duration', 'time_created', 'date_created', 'order_number']
        read_only_fields = ['id', 'time_created', 'date_created']

class TimeResourcesQueueSerializer(serializers.ModelSerializer):
    resource_item_name = serializers.SerializerMethodField()
    segment_name = serializers.SerializerMethodField()
    resource_model_name = serializers.SerializerMethodField()

    class Meta:
        model = TimeResourcesQueue
        fields = [
            'resource_item_code',
            'resource_item_name',
            'segment',
            'segment_name',
            'segment_start',
            'segment_end',
            'date_created',
            'resource_model',
            'resource_model_name',
            'segment_params',
            'order_number'
        ]

    def get_resource_item_name(self, obj):
        return obj.resource_item_code.name if obj.resource_item_code else None

    def get_segment_name(self, obj):
        if obj.segment and hasattr(obj.segment, 'modal_count'):
            logging.debug(f"Segment Name: {obj.segment.modal_count.name}")
            return obj.segment.modal_count.name
        else:
            logging.debug("Segment or ModalCount missing")
            return None

    def get_resource_model_name(self, obj):
        return obj.resource_model.name if obj.resource_model else None