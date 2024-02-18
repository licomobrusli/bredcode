# Generated by Django 5.0.2 on 2024-02-17 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0009_alter_resourceavailability_resource_item_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleModel',
            fields=[
                ('code', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'simple_model',
                'ordering': ['code'],
            },
        ),
    ]
