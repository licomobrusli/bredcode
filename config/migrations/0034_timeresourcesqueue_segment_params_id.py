# Generated by Django 4.2.7 on 2024-01-21 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0033_segmentparam_alter_timeresourcesqueue_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeresourcesqueue',
            name='segment_params_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='config.segmentparam'),
        ),
    ]
