# urls.py
from django.urls import path, include
from rest_framework import routers
from config.submit_order import create_order_and_items # Import the view function
from .views import (
    ServiceList,
    ServiceCategoryList,
    ModalCountList,
    ModalSelectList,
    OrdersList,
    OrderItemsList,
    TimeResourcesQueueViewSet,
)

router = routers.DefaultRouter()
router.register(r'time-resources-queue', TimeResourcesQueueViewSet)

urlpatterns = [
    path('service_categories/', ServiceCategoryList.as_view(), name='service_category_list'),
    path('services/', ServiceList.as_view(), name='services_list'),
    path('modal_counts/', ModalCountList.as_view(), name='modal_count_list'),
    path('modal_selects/', ModalSelectList.as_view(), name='modal_select_list'),
    path('orders/', OrdersList.as_view(), name='order_list'),
    path('order_items/', OrderItemsList.as_view(), name='order_items_list'),
    path('submit_order/', create_order_and_items, name='submit_order'),
    path('', include(router.urls)),
]
