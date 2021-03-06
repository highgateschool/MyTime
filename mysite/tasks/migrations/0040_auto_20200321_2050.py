# Generated by Django 3.0.2 on 2020-03-21 20:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0039_auto_20200320_1610'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserData',
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=datetime.date(2020, 3, 21), verbose_name='due date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_time',
            field=models.TimeField(default=datetime.time(20, 50, 1, 808826), verbose_name='due time'),
        ),
        migrations.AlterField(
            model_name='task',
            name='time_estimate',
            field=models.DurationField(default=datetime.timedelta(0), verbose_name='time estimate'),
        ),
    ]
