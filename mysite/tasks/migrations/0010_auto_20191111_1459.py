# Generated by Django 2.2.6 on 2019-11-11 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_auto_20191111_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(verbose_name='due date'),
        ),
    ]
