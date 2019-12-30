# Generated by Django 2.2.6 on 2019-12-01 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0024_task_priority'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField(verbose_name='date')),
                ('start_time', models.TimeField(verbose_name='start time')),
                ('end_time', models.TimeField(verbose_name='end time')),
            ],
        ),
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=200)),
                ('start_time', models.TimeField(verbose_name='start time')),
                ('end_time', models.TimeField(verbose_name='end time')),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='due_time',
        ),
        migrations.RemoveField(
            model_name='task',
            name='priority',
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(verbose_name='due date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='time_estimate',
            field=models.DurationField(verbose_name='time estimate'),
        ),
    ]
