# Generated by Django 5.1.4 on 2025-01-26 17:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_task_is_completed_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ManyToManyField(related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
