# Generated by Django 4.0.6 on 2022-08-01 20:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(choices=[('1', 'месяц'), ('2', '2 месяца'), ('3', '3 месяца'), ('6', 'пол года'), ('12', 'год')], default=1, max_length=255, verbose_name='Колличество месяцев')),
                ('data_start', models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')),
                ('data_end', models.DateTimeField(default=datetime.datetime(2022, 8, 2, 0, 25, 10, 797947), verbose_name='Дата окончания ')),
                ('price', models.CharField(blank=True, default='', help_text='Месяц - 1000.                                       2 Месяца - 1800.                                       3 Месяца - 2500.                                       Пол года - 4000.                                       Год - 8000.', max_length=255, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Абонимент в зал',
                'verbose_name_plural': 'Абонименты в зал',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Порядковый номер')),
                ('category', models.CharField(choices=[('Suite', 'Сюит'), ('Apartment', 'Апартамент '), ('Lux', 'Люкс '), ('Junior Suite', 'Джуниор Сюит'), ('Studio', 'Студия'), ('Standard', 'стандарт')], default='Standard', max_length=255, verbose_name='Категория номера')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=1, max_digits=8, verbose_name='Цена за ночь')),
                ('number_of_places', models.PositiveSmallIntegerField(verbose_name='Колличество мест')),
                ('free', models.BooleanField(default=True, help_text='True - в номере никто не проживаетFalse - на данный момент номер занят', verbose_name='Свободен')),
            ],
            options={
                'verbose_name': 'Номер',
                'verbose_name_plural': 'Номера',
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(db_index=True, max_length=255, verbose_name='Фамилия пользователя')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=255, region=None, verbose_name='Номер телефона')),
                ('adult', models.BooleanField(default=False, help_text='True - гость достиг совершенолетия. False - гость не достиг совершенолетия', verbose_name='Совершенолетие')),
                ('numbers_passport', models.PositiveBigIntegerField(null=True, verbose_name='Номер паспорта')),
                ('in_hotel', models.BooleanField(default=True, verbose_name='Проживает ли на данный момент')),
                ('check_in_time', models.DateField(auto_now_add=True, verbose_name='Врея заселения')),
                ('eviction_time', models.DateField(blank=True, default=None, null=True, verbose_name='Время выселения')),
                ('gym', models.ManyToManyField(blank=True, related_name='related_visitor', to='hotel.gym', verbose_name='Абонимент в спортзал')),
                ('number_room', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='hotel.room', verbose_name='Номер проживания')),
                ('online_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Онлайн аккаунт')),
            ],
            options={
                'verbose_name': 'Посетител',
                'verbose_name_plural': 'Посетители',
            },
        ),
        migrations.AddField(
            model_name='room',
            name='visitors',
            field=models.ManyToManyField(blank=True, to='hotel.visitor', verbose_name='Гости в номере'),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=1024, verbose_name='Тело текста отзыва')),
                ('file', models.FileField(blank=True, null=True, upload_to='reviews/%Y/%m/%d/', verbose_name='Прикрепленный файл к отзыву')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания отзыва')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления отзыва')),
                ('active', models.BooleanField(default=True, verbose_name='Состояние отзыва')),
                ('rating', models.CharField(blank=True, choices=[('1', 'terribly'), ('2', 'bad'), ('3', 'ok'), ('4', 'good'), ('5', 'amazing')], max_length=25, null=True, verbose_name='Рейтинг отеля')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор отзыва')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.AddField(
            model_name='gym',
            name='visitor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='related_gum', to='hotel.visitor', verbose_name='Гость'),
        ),
        migrations.CreateModel(
            name='ApplicationForRoomBron',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('True', 'Одобрена'), ('False', 'Откланенна'), ('in progress', 'В процессе обработки')], default='in progress', max_length=255, verbose_name='Статус заявки')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel.room', verbose_name='Желаемая комната на бронь')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец заявки на бронь')),
            ],
            options={
                'verbose_name': 'Заявка на бронь комнаты',
                'verbose_name_plural': 'Заявки на бронь комнаты',
            },
        ),
    ]
