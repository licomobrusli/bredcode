# Generated by Django 5.0.3 on 2024-03-14 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0006_timeresourcesqueue_staff_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeresourcesqueuehistory',
            name='staff_duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
