# Generated by Django 4.2.7 on 2024-02-05 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0071_resourceavailability_resource_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]