# Generated by Django 4.0.6 on 2022-08-05 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel', '0004_alter_applicationforroombron_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationforroombron',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец заявки на бронь'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор отзыва'),
        ),
    ]