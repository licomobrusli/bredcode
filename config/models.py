from django.db import models
from django.utils import timezone
import datetime

class ServiceCategory(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    image_path = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'service_categories' # Ensures the table name is exact
        ordering = ['id']  # Default ordering


class Services(models.Model):
    code = models.CharField(max_length=4, unique=True)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    total_duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_path = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'services' # Ensures the table name is exact
        ordering = ['id']  # Default ordering

class ModalSelect(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_code = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    service_code = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, blank=True)
    image_path = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'modal_select'  # Ensures the table name is exactly 'modal_select'
        ordering = ['id']  # Default ordering


class ModalCount(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_quantity = models.IntegerField()
    category_code = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    service_code = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, blank=True)
    image_path = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    logic = models.CharField(max_length=3, default='NOT', null=False)
    sub = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'modal_count'  # Ensures the table name is exactly 'ModalCount'
        ordering = ['id']  # Default ordering

class Orders(models.Model):
    item_count = models.IntegerField()
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    est_start = models.TimeField(auto_now_add=True, blank=True, null=True)
    est_duration = models.IntegerField(blank=True, null=True)
    start = models.TimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    time_created = models.TimeField(auto_now_add=True)
    date_created = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created
            now = timezone.now()
            self.est_start = now.time()  # Only save the time part
            self.time_created = now.time()  # Only save the time part
            self.date_created = now.date()  # Only save the date part
        super(Orders, self).save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):
    #    if not self.id:  # if new order
    #        last_order = Orders.objects.filter(date_created=datetime.date.today()).last()
    #        if last_order:
    #            self.est_start = (datetime.datetime.combine(datetime.date(1,1,1), last_order.est_start) + datetime.timedelta(minutes=last_order.est_duration)).time()
    #    super().save(*args, **kwargs)

    class Meta:
        db_table = 'orders'
        ordering = ['id']

class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    modal_count = models.ForeignKey(ModalCount, on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_count = models.IntegerField(blank=True, null=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    est_start = models.TimeField(auto_now_add=True, blank=True, null=True)
    est_duration = models.IntegerField(blank=True, null=True)
    start = models.TimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    time_created = models.TimeField(auto_now_add=True)
    date_created = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:  # If the object is being created
            now = timezone.now()
            self.est_start = now.time()  # Only save the time part
            self.time_created = now.time()  # Only save the time part
            self.date_created = now.date()  # Only save the date part
        super(OrderItems, self).save(*args, **kwargs)

    
    # def save(self, *args, **kwargs):
    #    if not self.id:  # if new order item
    #        last_item = OrderItems.objects.filter(order=self.order).last()
    #        if last_item:
    #            self.est_start = (datetime.datetime.combine(datetime.date(1,1,1), last_item.est_start) + datetime.timedelta(minutes=last_item.est_duration)).time()
    #    super().save(*args, **kwargs)

    class Meta:
        db_table = 'order_items'
        ordering = ['id']
