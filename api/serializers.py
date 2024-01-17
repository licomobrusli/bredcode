from rest_framework import serializers
from config.models import Services, ServiceCategory, ModalCount, ModalSelect, Orders, OrderItems

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
        fields = ['id', 'code', 'name', 'description', 'duration', 'price', 'max_quantity', 'category_code', 'service_code', 'image_path', 'date_created', 'logic', 'sub']

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