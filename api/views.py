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
        services = Services.objects.all()
        category_code = self.request.query_params.get('categoryCode', None)
        if category_code:
            # Assuming that your ServiceCategory model has a 'code' field that is unique for each category
            services = services.filter(service_category__code=category_code)
        serializer = ServicesSerializer(services, many=True)
        return Response(serializer.data)
