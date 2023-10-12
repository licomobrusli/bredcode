from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config.models import ServiceCategory
from .serializers import ServiceCategorySerializer

class ServiceCategoryList(APIView):
    def get(self, request, format=None):
        categories = ServiceCategory.objects.all()
        serializer = ServiceCategorySerializer(categories, many=True)
        return Response(serializer.data)
