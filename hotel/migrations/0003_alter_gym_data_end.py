# Generated by Django 4.0.6 on 2022-08-03 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_remove_room_free_remove_room_visitors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='data_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания '),
        ),
    ]