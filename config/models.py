from django.db import models

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
        db_table = 'modal_count'  # Ensures the table name is exactly 'modal_count'
        ordering = ['id']  # Default ordering