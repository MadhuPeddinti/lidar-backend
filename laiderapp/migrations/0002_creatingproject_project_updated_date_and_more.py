# Generated by Django 4.0.3 on 2022-04-06 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laiderapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatingproject',
            name='PROJECT_UPDATED_DATE',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='las_files',
            name='TASK_UPDATED_DATE',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
