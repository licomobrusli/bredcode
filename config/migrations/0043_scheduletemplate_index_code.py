# Generated by Django 4.2.7 on 2024-01-28 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0042_remove_scheduletemplate_index_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduletemplate',
            name='index_code',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='config.scheduletemplateindex'),
            preserve_default=False,
        ),
    ]
