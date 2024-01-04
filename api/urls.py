# urls.py
from django.urls import path
from .views import ServiceList, ServiceCategoryList, ModalCountList, ModalSelectList

urlpatterns = [
    path('service_categories/', ServiceCategoryList.as_view(), name='service_category_list'),
    path('services/', ServiceList.as_view(), name='services_list'),
    path('modal_counts/', ModalCountList.as_view(), name='modal_count_list'),
    path('modal_selects/', ModalSelectList.as_view(), name='modal_select_list'),
]
