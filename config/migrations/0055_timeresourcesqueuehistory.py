# Generated by Django 4.2.7 on 2024-01-30 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0054_remove_resourcemodel_type_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeResourcesQueueHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_item_code', models.CharField(max_length=25)),
                ('segment', models.CharField(max_length=50)),
                ('segment_start', models.DateTimeField()),
                ('segment_end', models.DateTimeField()),
                ('date_created', models.DateField()),
                ('archived_date', models.DateTimeField(auto_now_add=True)),
                ('resource_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='config.resourcemodel')),
                ('segment_params', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.segmentparam')),
            ],
            options={
                'db_table': 'time_resources_queue_history',
                'ordering': ['archived_date'],
            },
        ),
    ]
