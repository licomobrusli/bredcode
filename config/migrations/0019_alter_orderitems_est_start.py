# Generated by Django 4.2.7 on 2024-01-05 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0018_alter_orders_est_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='est_start',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
