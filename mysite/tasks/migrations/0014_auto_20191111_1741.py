# Generated by Django 2.2.6 on 2019-11-11 17:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_auto_20191111_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2019, 11, 11, 17, 41, 38, 734334, tzinfo=utc), verbose_name='due date'),
        ),
    ]
