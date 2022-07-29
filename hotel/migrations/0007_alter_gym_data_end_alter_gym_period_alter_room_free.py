# Generated by Django 4.0.6 on 2022-07-29 12:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_visitor_first_name_visitor_last_name_visitor_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='data_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 29, 16, 16, 42, 872543), verbose_name='Дата окончания '),
        ),
        migrations.AlterField(
            model_name='gym',
            name='period',
            field=models.PositiveIntegerField(choices=[('1', 'месяц'), ('2', '2 месяца'), ('3', '3 месяца'), ('6', 'пол года'), ('12', 'год')], default=1, verbose_name='Колличество месяцев'),
        ),
        migrations.AlterField(
            model_name='room',
            name='free',
            field=models.BooleanField(default=True, help_text='True - в номере никто не проживаетFalse - на данный момент номер занят', verbose_name='Свободен'),
        ),
    ]
