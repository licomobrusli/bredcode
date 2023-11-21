# admin.py
from django.contrib import admin
from .models import ServiceCategory, Services, ModalCount

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description', 'image_path', 'date_created']
    search_fields = ['code', 'name']
    list_filter = ['date_created']

admin.site.register(ServiceCategory, ServiceCategoryAdmin)

class ServicesAdmin(admin.ModelAdmin):
    list_display = ['code', 'service_category', 'name', 'description', 'total_duration', 'price', 'image_path', 'date_created']
    search_fields = ['code', 'service_category', 'name']
    list_filter = ['date_created', 'service_category']

admin.site.register(Services, ServicesAdmin)

class ModalCountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description', 'duration', 'price', 'max_quantity', 'category_code', 'service_code', 'image_path', 'date_created', 'logic']
    search_fields = ['code', 'name', 'category_code__name', 'service_code__name']
    list_filter = ['date_created', 'category_code', 'service_code']

admin.site.register(ModalCount, ModalCountAdmin)
