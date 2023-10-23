from rest_framework import serializers
from config.models import Services, ServiceCategory

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['code', 'name', 'description', 'image_path', 'date_created']

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id', 'name', 'description', 'price', 'duration', 'image_path', 'date_created']
