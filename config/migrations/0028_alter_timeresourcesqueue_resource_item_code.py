# Generated by Django 4.2.7 on 2024-01-21 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0027_alter_timeresourcesqueue_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeresourcesqueue',
            name='resource_item_code',
            field=models.CharField(max_length=25),
        ),
    ]
