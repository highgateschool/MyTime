# Generated by Django 2.2.6 on 2019-11-05 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20191104_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time_estimate',
            field=models.TimeField(verbose_name='time estimate'),
        ),
    ]
