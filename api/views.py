# views.py
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from config.models import ServiceCategory, Services, ModalCount, ModalSelect, Orders, OrderItems
from .serializers import  ServiceCategorySerializer, ServicesSerializer, ModalCountSerializer, ModalSelectSerializer, OrdersSerializer, OrderItemsSerializer

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
        code = request.query_params.get('code', None)  # New line to get the code parameter

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
    
class OrdersList(APIView):
    def get(self, request, format=None):
        orders = Orders.objects.all()

        # Get id from query parameters
        id = request.query_params.get('id', None)

        # Filter by id if provided
        if id:
            orders = orders.filter(id__code=id)

        serializer = OrdersSerializer(orders, many=False)
        return Response(serializer.data)

class OrderCreate(CreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class OrderItemsList(APIView):
    def get(self, request, format=None):
        order_items = OrderItems.objects.all()

        # Get order from query parameters
        id = request.query_params.get('id', None)
        order = request.query_params.get('order', None)

        # Filter by id if provided
        if id:
            order_items = order_items.filter(id__code=id)
            
        # Filter by order if provided
        if order:
            order_items = order_items.filter(order__id=order)

        serializer = OrderItemsSerializer(order_items, many=False)
        return Response(serializer.data)
    
class OrderItemCreate(CreateAPIView):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer


@api_view(['POST'])
def create_order_and_items(request):
    with transaction.atomic():
        order_data = request.data.get('order')

        # Create an order instance in memory with the received order_number
        order = Orders(
            item_count=order_data['item_count'],
            order_price=order_data['order_price'],
            order_number=order_data.get('order_number')  # Use the received order number
        )
        order.save()

        for item_data in request.data.get('items', []):
            modal_count_instance = get_object_or_404(ModalCount, id=item_data['modal_count'])
            OrderItems.objects.create(
                order=order,
                modal_count=modal_count_instance,  # Use the fetched ModalCount instance
                item_name=item_data['item_name'],
                unit_price=item_data['unit_price'],
                item_count=item_data['item_count'],
                item_price=item_data['item_price'],
            )

        # Ensure you return a Response object
        return Response({'status': 'OK', 'order_number': order.order_number})
