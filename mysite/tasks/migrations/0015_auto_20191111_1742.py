# Generated by Django 2.2.6 on 2019-11-11 17:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_auto_20191111_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=datetime.date(2019, 11, 11), verbose_name='due date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_time',
            field=models.TimeField(default=datetime.time(17, 42, 38, 375366), verbose_name='due time'),
        ),
    ]
