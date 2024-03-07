# Generated by Django 5.0.2 on 2024-03-04 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0017_timeresourcesqueue_staff_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modalcount',
            name='code',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='phaseresource',
            name='code',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='phase_resource', to='config.segment'),
        ),
    ]