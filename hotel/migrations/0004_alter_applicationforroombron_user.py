# Generated by Django 4.0.6 on 2022-08-05 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel', '0003_alter_gym_data_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationforroombron',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец заявки на бронь'),
        ),
    ]
