# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from config.models import ServiceCategory, Services, ModalCount
from .serializers import  ServiceCategorySerializer, ServicesSerializer, ModalCountSerializer
from config.models import ModalSelect
from .serializers import ModalSelectSerializer

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
    
class ModalCountList(APIView):
    def get(self, request, format=None):
        modal_counts = ModalCount.objects.all()

        # Get category_code and service_code from query parameters
        category_code = request.query_params.get('categoryCode', None)
        service_code = request.query_params.get('serviceCode', None)

        # Filter by category code if provided
        if category_code:
            modal_counts = modal_counts.filter(category_code__code=category_code)

        # Filter by service code if provided
        if service_code:
            modal_counts = modal_counts.filter(service_code__code=service_code)

        serializer = ModalCountSerializer(modal_counts, many=True)
        return Response(serializer.data)
    
class ModalSelectList(APIView):
    def get(self, request, format=None):
        modal_selects = ModalSelect.objects.all()

        # Get category_code and service_code from query parameters
        category_code = request.query_params.get('categoryCode', None)
        service_code = request.query_params.get('serviceCode', None)
        code = request.query_params.get('code', None)  # New line to get the codeStart parameter

        # Filter by category code if provided
        if category_code:
            modal_selects = modal_selects.filter(category_code__code=category_code)

        # Filter by service code if provided
        if service_code:
            modal_selects = modal_selects.filter(service_code__code=service_code)

        # New block: Filter by code field if provided
        if code:
            modal_selects = modal_selects.filter(code__startswith=code)

        serializer = ModalSelectSerializer(modal_selects, many=True)
        return Response(serializer.data)
    