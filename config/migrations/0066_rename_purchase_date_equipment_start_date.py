# Generated by Django 4.2.7 on 2024-02-01 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0065_timeresourceitems_end_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment',
            old_name='purchase_date',
            new_name='start_date',
        ),
    ]