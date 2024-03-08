# admin.py
from django.contrib import admin
from .models import ServiceCategory, Services, ModalCount, ModalSelect, Orders, OrderItems, Employee

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
    list_display = ['code', 'name', 'description', 'duration', 'price', 'max_quantity', 'category_code', 'service_code', 'image_path', 'date_created', 'logic', 'sub']
    search_fields = ['code', 'name', 'category_code__name', 'service_code__name']
    list_filter = ['date_created', 'category_code', 'service_code']

admin.site.register(ModalCount, ModalCountAdmin)

class ModalSelectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description', 'duration', 'price', 'category_code', 'service_code', 'image_path', 'date_created']
    search_fields = ['code', 'name', 'category_code__name', 'service_code__name']
    list_filter = ['date_created', 'category_code', 'service_code']

admin.site.register(ModalSelect, ModalSelectAdmin)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ['item_count', 'order_price', 'est_start', 'est_duration', 'start', 'duration', 'time_created', 'date_created', 'order_number']
    search_fields = ['id']
    list_filter = ['date_created']

admin.site.register(Orders, OrdersAdmin)

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'modal_count', 'item_name', 'unit_price', 'item_count', 'item_price', 'est_start', 'est_duration', 'start', 'duration', 'time_created', 'date_created', 'order_number']
    search_fields = ['order']
    list_filter = ['order', 'date_created']

admin.site.register(OrderItems, OrderItemsAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'dni', 'naf', 'dob', 'tel', 'email', 'street', 'town', 'postcode', 'resource_item', 'resource_model']
    search_fields = ['name', 'surname', 'dni', 'naf']
    list_filter = ['resource_item', 'resource_model']

admin.site.register(Employee, EmployeeAdmin)