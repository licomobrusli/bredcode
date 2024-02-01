from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('config', '0062_rename_role_employee_resource_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='equipment',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='employee',
            name='code',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='code',
        ),
        migrations.AddField(
            model_name='employee',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='resource_item',
            field=models.CharField(max_length=25, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipment',
            name='resource_item',
            field=models.CharField(max_length=25, unique=True, null=True, blank=True),
        ),
    ]
