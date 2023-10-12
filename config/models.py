from django.db import models

class ServiceCategory(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    image_path = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'service_categories'
