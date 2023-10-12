from rest_framework import serializers
from config.models import ServiceCategory

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['code', 'name', 'description', 'image_path', 'date_created']
