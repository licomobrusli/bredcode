# Generated by Django 4.2.7 on 2024-01-26 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0037_alter_orderitems_est_start_alter_orderitems_start_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourceavailability',
            name='resource_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.timeresourcesqueue'),
        ),
    ]
