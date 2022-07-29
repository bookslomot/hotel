# Generated by Django 4.0.6 on 2022-07-29 12:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0007_alter_gym_data_end_alter_gym_period_alter_room_free'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 29, 16, 27, 0, 162649), verbose_name='Дата окончания '),
        ),
        migrations.AlterField(
            model_name='gym',
            name='period',
            field=models.CharField(choices=[('1', 'месяц'), ('2', '2 месяца'), ('3', '3 месяца'), ('6', 'пол года'), ('12', 'год')], default=1, max_length=255, verbose_name='Колличество месяцев'),
        ),
    ]