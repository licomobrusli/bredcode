# Generated by Django 4.2.7 on 2024-02-05 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0076_alter_orders_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_number',
            field=models.CharField(max_length=20),
        ),
    ]