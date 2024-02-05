# Generated by Django 4.2.7 on 2024-02-03 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0070_alter_equipment_resource_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourceavailability',
            name='resource_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='config.resourcemodel'),
        ),
    ]