# Generated by Django 3.0.2 on 2020-03-20 15:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0037_auto_20200320_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_in_time',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_time',
            field=models.TimeField(default=datetime.time(15, 58, 31, 23602), verbose_name='due time'),
        ),
    ]
