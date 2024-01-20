# Generated by Django 4.2.7 on 2024-01-20 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0024_resourcetype_resourcemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('sequence', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('item_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.modalcount')),
            ],
            options={
                'db_table': 'phases',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PhaseResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('phase_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.phase')),
                ('resource_models_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.resourcemodel')),
            ],
            options={
                'db_table': 'phase_resources',
                'ordering': ['id'],
            },
        ),
    ]
