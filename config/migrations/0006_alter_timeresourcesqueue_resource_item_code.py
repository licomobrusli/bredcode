# Generated by Django 5.0.2 on 2024-02-17 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0005_alter_timeresourcesqueue_resource_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeresourcesqueue',
            name='resource_item_code',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]