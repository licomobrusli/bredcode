from rest_framework import serializers
from config.models import Services, ServiceCategory, ModalCount

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
        fields = ['id', 'code', 'name', 'description', 'duration', 'price', 'max_quantity', 'category_code', 'service_code', 'image_path', 'date_created', 'logic']
