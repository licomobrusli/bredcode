# views.py
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from forms.register_user import EmployeeRegistrationForm
from config.models import ServiceCategory, Services, ModalCount, ModalSelect, Orders, OrderItems, TimeResourcesQueue, Employee, TimeResourceItems
from .serializers import  ServiceCategorySerializer, ServicesSerializer, ModalCountSerializer, ModalSelectSerializer, OrdersSerializer, OrderItemsSerializer, TimeResourcesQueueSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from django.core.serializers import serialize
from django.utils.dateparse import parse_datetime
from datetime import timedelta
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

@method_decorator(csrf_exempt, name='dispatch')
class RegisterEmployeeView(APIView):
    def post(self, request, *args, **kwargs):
        logging.info("Received registration request with data: {}".format(request.data))
        form = EmployeeRegistrationForm(request.data)  # Use request.data instead of request.POST for JSON data
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

            logging.info("User registration successful for: {}".format(user.username))
            return JsonResponse({'status': 'success', 'user_id': user.id})
        else:
            logging.error("Registration form invalid: {}".format(form.errors))
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400) 
    
    def get(self, request, *args, **kwargs):
        # Handle GET request if necessary, otherwise just return an error
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are accepted'})
    
@method_decorator(csrf_exempt, name='dispatch')
class LoginEmployeeView(APIView):
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Received login request with data: {}")
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')  # For logging purposes, be cautious about logging plain passwords

        logging.info(f"Received login request for username: {username}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                logging.debug(f"Login successful for user: {username}")
                return Response({'status': 'success', 'user_id': user.id, 'token': token.key})
            else:
                logging.debug(f"Login failed for user: {username} - User is not active")
                return Response({'status': 'error', 'message': 'User is not active'})
        else:
            logging.debug(f"Login failed for user: {username} - Invalid username or password")
            return Response({'status': 'error', 'message': 'Invalid username or password'})
        
@method_decorator(csrf_exempt, name='dispatch')
class LogoutEmployeeView(APIView):
    def post(self, request, *args, **kwargs):
        # Log the user out
        logging.info(f"Received logout request from user: {request.user.username}")
        logout(request)
        logging.debug(f"Logout successful for user: {request.user.username}")
        return Response({'status': 'success', 'message': 'Logged out successfully'})

    def get(self, request, *args, **kwargs):
        # Optionally, handle GET request if necessary, otherwise just return an error
        return Response({'status': 'error', 'message': 'Only POST requests are accepted'})
    pass

class UserTimeResourcesQueueList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        try:
            # First, get the employee related to this user
            employee = Employee.objects.get(resource_item__resource_item_code=user.username)
            # Then, filter TimeResourcesQueue by the employee's resource item
            time_resources = TimeResourcesQueue.objects.filter(resource_item_code=employee.resource_item)
            serializer = TimeResourcesQueueSerializer(time_resources, many=True)
            
            # Use Django's serializer to convert queryset into JSON string for logging
            serialized_time_resources = serialize('json', time_resources)
            logging.debug("Fetched time resources: %s", serialized_time_resources)
            
            return Response(serializer.data)
        except Employee.DoesNotExist:
            logging.error('Employee with this user does not exist or has no resource items assigned')
            return Response({'error': 'Employee with this user does not exist or has no resource items assigned'}, status=404)

        
class UpdateTimeResource(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, time_resource_id):
        # Extract data from the request
        staff_start = request.data.get('staff_start')
        staff_end = request.data.get('staff_end')
        staff_timer = request.data.get('staff_timer', 0)  # Default to 0 if not provided

        # Convert staff_start and staff_end from ISO 8601 string to datetime objects
        if staff_start:
            staff_start = parse_datetime(staff_start)
        if staff_end:
            staff_end = parse_datetime(staff_end)

        # Convert staff_timer from seconds to a timedelta object
        staff_timer = timedelta(seconds=int(staff_timer))

        try:
            # Get the TimeResource instance and update its fields
            time_resource = TimeResourcesQueue.objects.get(pk=time_resource_id)
            if staff_start:
                time_resource.staff_start = staff_start
            if staff_end:
                time_resource.staff_end = staff_end
            time_resource.staff_timer = staff_timer  # Assuming you want to overwrite even if it's zero

            # Save the updated instance
            time_resource.save()

            # Respond with the updated information
            return Response({
                'id': time_resource.id,
                'staff_start': time_resource.staff_start.isoformat() if time_resource.staff_start else None,
                'staff_end': time_resource.staff_end.isoformat() if time_resource.staff_end else None,
                'staff_timer': time_resource.staff_timer.total_seconds() if time_resource.staff_timer else None,
            })
        except TimeResourcesQueue.DoesNotExist:
            return Response({'error': 'TimeResource not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
