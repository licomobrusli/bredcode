from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config.models import ServiceCategory, Services  # <-- Import Services model here
from .serializers import ServiceCategorySerializer, ServicesSerializer  # <-- Import ServicesSerializer here

class ServiceCategoryList(APIView):
    def get(self, request, format=None):
        categories = ServiceCategory.objects.all()
        serializer = ServiceCategorySerializer(categories, many=True)
        return Response(serializer.data)

class ServiceList(APIView):
    def get(self, request, format=None):
        services = Services.objects.all()  # <-- Use Services here
        service_category_id = self.request.query_params.get('service_category_id', None)
        if service_category_id:
            services = services.filter(service_category_id=service_category_id)
        serializer = ServicesSerializer(services, many=True)  # <-- Use ServicesSerializer here
        return Response(serializer.data)
