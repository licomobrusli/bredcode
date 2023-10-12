from django.urls import path
from .views import ServiceCategoryList

urlpatterns = [
    path('service_categories/', ServiceCategoryList.as_view(), name='service_category_list'),
]
