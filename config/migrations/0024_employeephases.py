# Generated by Django 5.0.2 on 2024-03-08 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0023_timeresourcesqueue_staff_timer'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeePhases',
            fields=[
                ('employee_phase', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('avg_duration', models.IntegerField(blank=True, null=True)),
                ('avg_score', models.FloatField(blank=True, null=True)),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('phase_resource_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_phases', to='config.phase')),
                ('resource_item_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_phases', to='config.timeresourceitems')),
                ('resource_model_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_phases', to='config.resourcemodel')),
            ],
            options={
                'db_table': 'employee_phases',
                'ordering': ['employee_phase'],
            },
        ),
    ]
