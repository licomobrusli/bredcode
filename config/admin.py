from django.contrib import admin
from .models import ServiceCategory, Services

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description', 'image_path', 'date_created']
    search_fields = ['code', 'name']
    list_filter = ['date_created']

admin.site.register(ServiceCategory, ServiceCategoryAdmin)

class ServicesAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description', 'total_duration', 'price', 'image_path', 'date_created']
    search_fields = ['code', 'name']
    list_filter = ['date_created']

admin.site.register(Services, ServicesAdmin)
