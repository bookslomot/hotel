# Generated by Django 4.0.6 on 2022-08-11 15:36

from django.conf import settings
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel', '0005_alter_applicationforroombron_user_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reviews',
            new_name='Review',
        ),
        migrations.AlterField(
            model_name='visitor',
            name='first_name',
            field=models.CharField(default='online_client__first_name', max_length=255, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='last_name',
            field=models.CharField(default='online_client__last_name', max_length=255, verbose_name='Фамилия пользователя'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default='online_client__phone', max_length=255, region=None, verbose_name='Номер телефона'),
        ),
    ]
