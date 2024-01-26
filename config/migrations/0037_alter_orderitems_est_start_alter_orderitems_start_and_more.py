from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('config', '0036_resourceavailability'),
    ]

    operations = [
        # OrderItems: Remove TimeFields
        migrations.RemoveField(
            model_name='orderitems',
            name='est_start',
        ),
        migrations.RemoveField(
            model_name='orderitems',
            name='start',
        ),
        migrations.RemoveField(
            model_name='orderitems',
            name='time_created',
        ),
        # Orders: Remove TimeFields
        migrations.RemoveField(
            model_name='orders',
            name='est_start',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='start',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='time_created',
        ),
        # TimeResourcesQueue: Remove TimeFields
        migrations.RemoveField(
            model_name='timeresourcesqueue',
            name='segment_end',
        ),
        migrations.RemoveField(
            model_name='timeresourcesqueue',
            name='segment_start',
        ),

        # OrderItems: Add DateTimeFields
        migrations.AddField(
            model_name='orderitems',
            name='est_start',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        # Orders: Add DateTimeFields
        migrations.AddField(
            model_name='orders',
            name='est_start',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        # TimeResourcesQueue: Add DateTimeFields
        migrations.AddField(
            model_name='timeresourcesqueue',
            name='segment_end',
            field=models.DateTimeField(),
        ),
        migrations.AddField(
            model_name='timeresourcesqueue',
            name='segment_start',
            field=models.DateTimeField(),
        ),
    ]
