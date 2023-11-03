from rest_framework import serializers
from config.models import Services, ServiceCategory

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'code', 'name', 'description', 'image_path', 'date_created']

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id', 'code', 'name', 'description', 'price', 'total_duration', 'image_path', 'service_category', 'date_created']
