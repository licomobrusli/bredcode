# views.py
from django.db import transaction
from django.views import View
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.auth.models import Group
from forms.register_user import EmployeeRegistrationForm
from config.models import Employee
from config.models import ServiceCategory, Services, ModalCount, ModalSelect, Orders, OrderItems, TimeResourcesQueue, Employee
from .serializers import  ServiceCategorySerializer, ServicesSerializer, ModalCountSerializer, ModalSelectSerializer, OrdersSerializer, OrderItemsSerializer, TimeResourcesQueueSerializer
import logging

class ServiceCategoryList(APIView):
    def get(self, request, format=None):
        logging.debug('ServiceCategoryList #############################')
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

# class OrderCreate(CreateAPIView):
#     queryset = Orders.objects.all()
#     serializer_class = OrdersSerializer

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
    
class TimeResourcesQueueViewSet(viewsets.ModelViewSet):
    queryset = TimeResourcesQueue.objects.all()
    serializer_class = TimeResourcesQueueSerializer

class RegisterEmployeeView(View):
    def post(self, request, *args, **kwargs):
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Saves the User instance
            employee = Employee.objects.get(resource_item=form.cleaned_data['username'])
            user.first_name = employee.name
            user.last_name = employee.surname
            user.email = employee.email
            user.save()

            # Assign user to a group based on their role
            group_name = employee.resource_model  # Assuming this matches your Group name
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            # Instead of redirecting, return a success response
            return JsonResponse({'status': 'success', 'user_id': user.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    def get(self, request, *args, **kwargs):
        # Handle GET request if necessary, otherwise just return an error
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are accepted'})