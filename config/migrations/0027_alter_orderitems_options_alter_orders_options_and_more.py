# Generated by Django 5.0.3 on 2024-03-08 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0026_alter_servicecategory_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitems',
            options={'ordering': ['id'], 'verbose_name': 'Order Item'},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'ordering': ['id'], 'verbose_name': 'Order'},
        ),
        migrations.AlterModelOptions(
            name='services',
            options={'ordering': ['id'], 'verbose_name': 'Service'},
        ),
    ]
