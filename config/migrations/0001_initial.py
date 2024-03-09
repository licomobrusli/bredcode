# Generated by Django 5.0.3 on 2024-03-09 22:11

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeResourceItems',
            fields=[
                ('resource_item_code', models.CharField(max_length=25, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(default=datetime.date.today)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'time_resource_items',
                'ordering': ['resource_item_code'],
            },
        ),
        migrations.CreateModel(
            name='ModalCount',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('duration', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_quantity', models.IntegerField()),
                ('image_path', models.CharField(blank=True, max_length=1000, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('logic', models.CharField(default='NOT', max_length=3)),
                ('sub', models.IntegerField(default=0)),
                ('sequence', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'modal_count',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_count', models.IntegerField()),
                ('order_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('est_start', models.DateTimeField(auto_now_add=True, null=True)),
                ('est_duration', models.IntegerField(blank=True, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('order_number', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Order',
                'db_table': 'orders',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'segments',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='ResourceModel',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('cost_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('no_of_units', models.IntegerField()),
                ('fungible', models.BooleanField(default=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'resource_models',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('measure', models.CharField(max_length=100)),
                ('unit_size', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'resource_types',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleTemplateIndex',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('rotations', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'schedule_template_index',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='SegmentParam',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('container', models.BooleanField(default=False)),
                ('contained', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=False)),
                ('working', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('calc_pay', models.IntegerField(default=0)),
                ('calc_available', models.IntegerField(default=0)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'segment_params',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('image_path', models.CharField(blank=True, max_length=1000, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Service Categories',
                'db_table': 'service_categories',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('resource_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='employees', serialize=False, to='config.timeresourceitems')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=10, unique=True)),
                ('naf', models.CharField(max_length=15, unique=True)),
                ('dob', models.DateField()),
                ('tel', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('street', models.CharField(blank=True, max_length=255, null=True)),
                ('town', models.CharField(max_length=100)),
                ('postcode', models.CharField(blank=True, max_length=10, null=True)),
                ('resource_model', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'employees',
                'ordering': ['resource_item'],
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item_count', models.IntegerField(blank=True, null=True)),
                ('item_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('est_start', models.DateTimeField(auto_now_add=True, null=True)),
                ('est_duration', models.IntegerField(blank=True, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('order_number', models.CharField(blank=True, max_length=20)),
                ('modal_count', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.modalcount')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='config.orders')),
            ],
            options={
                'verbose_name': 'Order Item',
                'db_table': 'order_items',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('sequence', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('modal_count', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.modalcount')),
            ],
            options={
                'db_table': 'phases',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleElements',
            fields=[
                ('code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='schedule_elements', serialize=False, to='config.segment')),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField()),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'schedule_elements',
                'ordering': ['code'],
            },
        ),
        migrations.AddField(
            model_name='timeresourceitems',
            name='resource_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.resourcemodel'),
        ),
        migrations.CreateModel(
            name='ResourceAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_start', models.DateTimeField()),
                ('available_end', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('resource_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.timeresourceitems')),
                ('resource_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.resourcemodel')),
            ],
            options={
                'db_table': 'resource_availablity',
                'ordering': ['date_created', 'available_start'],
            },
        ),
        migrations.AddField(
            model_name='resourcemodel',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='config.resourcetype'),
        ),
        migrations.CreateModel(
            name='ScheduleTemplate',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('wk', models.CharField(max_length=1)),
                ('wkday', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)])),
                ('shift_start', models.TimeField()),
                ('shift_end', models.TimeField()),
                ('sched_container', models.DurationField()),
                ('lunch_duration', models.DurationField(blank=True, null=True)),
                ('gross_sched', models.DurationField()),
                ('breaks_duration', models.DurationField(blank=True, null=True)),
                ('net_sched', models.DurationField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('index_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.scheduletemplateindex')),
            ],
            options={
                'db_table': 'schedule_templates',
                'ordering': ['code'],
            },
        ),
        migrations.AddField(
            model_name='segment',
            name='segment_param',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='segments', to='config.segmentparam'),
        ),
        migrations.AddField(
            model_name='modalcount',
            name='category_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.servicecategory'),
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('total_duration', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image_path', models.CharField(blank=True, max_length=1000, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('service_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.servicecategory')),
            ],
            options={
                'verbose_name': 'Service',
                'db_table': 'services',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='ModalSelect',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('duration', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image_path', models.CharField(blank=True, max_length=1000, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('category_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.servicecategory')),
                ('service_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.services')),
            ],
            options={
                'db_table': 'modal_select',
                'ordering': ['code'],
            },
        ),
        migrations.AddField(
            model_name='modalcount',
            name='service_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.services'),
        ),
        migrations.CreateModel(
            name='TimeResourceScheduleIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_rotation', models.CharField(max_length=1)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('resource_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.timeresourceitems')),
                ('resource_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.resourcemodel')),
                ('schedule_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.scheduletemplateindex')),
            ],
            options={
                'db_table': 'time_resource_schedule_index',
            },
        ),
        migrations.CreateModel(
            name='TimeResourcesQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('segment_name', models.CharField(max_length=100)),
                ('segment_start', models.DateTimeField()),
                ('segment_end', models.DateTimeField()),
                ('staff_start', models.DateTimeField(blank=True, null=True)),
                ('staff_end', models.DateTimeField(blank=True, null=True)),
                ('staff_timer', models.DurationField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('order_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.orders', to_field='order_number')),
                ('resource_item_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.timeresourceitems')),
                ('resource_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.resourcemodel')),
                ('segment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_resources_queue', to='config.segment')),
                ('segment_params', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='config.segmentparam')),
            ],
            options={
                'db_table': 'time_resources_queue',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TimeResourcesQueueHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_id', models.IntegerField()),
                ('segment', models.CharField(max_length=50)),
                ('segment_name', models.CharField(blank=True, max_length=100, null=True)),
                ('segment_start', models.DateTimeField()),
                ('segment_end', models.DateTimeField()),
                ('staff_start', models.DateTimeField(blank=True, null=True)),
                ('staff_end', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateField()),
                ('archived_date', models.DateTimeField(auto_now_add=True)),
                ('order_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.orders', to_field='order_number')),
                ('resource_item_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.timeresourceitems')),
                ('resource_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.resourcemodel')),
                ('segment_params', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.segmentparam')),
            ],
            options={
                'db_table': 'time_resources_queue_history',
                'ordering': ['archived_date'],
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('resource_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='equipment', serialize=False, to='config.timeresourceitems')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('resource_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.resourcemodel')),
            ],
            options={
                'db_table': 'equipment',
                'ordering': ['resource_item'],
            },
        ),
        migrations.CreateModel(
            name='PhaseResource',
            fields=[
                ('code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='phase_resource', serialize=False, to='config.segment')),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('phase_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='config.phase')),
                ('resource_models_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.resourcemodel')),
                ('resource_types_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.resourcetype')),
            ],
            options={
                'db_table': 'phase_resources',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='EmployeePhases',
            fields=[
                ('employee_phase', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('avg_duration', models.IntegerField(blank=True, null=True)),
                ('avg_score', models.FloatField(blank=True, null=True)),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('resource_model_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_phases', to='config.resourcemodel')),
                ('resource_item_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_phases', to='config.employee')),
                ('phase_resource_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_phases', to='config.phaseresource')),
            ],
            options={
                'db_table': 'employee_phases',
                'ordering': ['employee_phase'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='timeresourceitems',
            unique_together={('resource_item_code', 'start_date', 'end_date')},
        ),
    ]
