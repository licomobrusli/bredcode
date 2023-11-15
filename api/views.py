# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config.models import ServiceCategory, Services  # <-- Import Services model here
from .serializers import ServiceCategorySerializer, ServicesSerializer  # <-- Import ServicesSerializer here

class ServiceCategoryList(APIView):
    def get(self, request, format=None):
        category_code = request.query_params.get('categoryCode', None)
        if category_code:
            categories = ServiceCategory.objects.filter(code=category_code)[:1]
        else:
            categories = ServiceCategory.objects.all()
        serializer = ServiceCategorySerializer(categories, many=True)
        return Response(serializer.data)

class ServiceList(APIView):
    def get(self, request, format=None):
        services = Services.objects.all()

        # Get category_code and service_code from query parameters
        category_code = request.query_params.get('categoryCode', None)
        service_code = request.query_params.get('serviceCode', None)

        # Filter by category code if provided
        if category_code:
            services = services.filter(service_category__code=category_code)

        # Filter by service code if provided
        if service_code:
            services = services.filter(code=service_code)

        serializer = ServicesSerializer(services, many=True)
        return Response(serializer.data)