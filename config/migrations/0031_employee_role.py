# Generated by Django 4.2.7 on 2024-01-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0030_modalcount_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='role',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
