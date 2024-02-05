# Generated by Django 4.2.7 on 2024-02-01 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0068_remove_employee_end_date_remove_employee_start_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='time_resource_item',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='employee',
            name='resource_item',
            field=models.ForeignKey(default='dmontoya', on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='config.timeresourceitems'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='resource_item',
            field=models.ForeignKey(default='dmontoya', on_delete=django.db.models.deletion.CASCADE, related_name='equipment', to='config.timeresourceitems', verbose_name='Time Resource Item'),
            preserve_default=False,
        ),
    ]