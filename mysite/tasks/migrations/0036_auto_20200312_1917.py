# Generated by Django 3.0.2 on 2020-03-12 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0035_auto_20200308_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=datetime.date(2020, 3, 12), verbose_name='due date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_time',
            field=models.TimeField(default=datetime.time(19, 17, 18, 686332), verbose_name='due time'),
        ),
    ]
