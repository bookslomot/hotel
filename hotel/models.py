import datetime
from django.db import models
from phonenumber_field import modelfields

from hotel.services import set_data_end_gym, set_price, check_in_hotel_visitor, read_price_json_from_txt
from user.models import User


class Room(models.Model):
    CAT_CHOICES = (
        ('Suite', 'Сюит'),
        ('Apartment', 'Апартамент '),
        ('Lux', 'Люкс '),
        ('Junior Suite', 'Джуниор Сюит'),
        ('Studio', 'Студия'),
        ('Standard', 'стандарт'),

    )

    number = models.PositiveIntegerField('Порядковый номер')
    category = models.CharField('Категория номера',
                                choices=CAT_CHOICES,
                                max_length=255,
                                blank=False,
                                default='Standard')
    price = models.DecimalField('Цена за ночь', max_digits=8, decimal_places=2, default=1, blank=True)
    number_of_places = models.PositiveSmallIntegerField('Колличество мест')
    free = models.BooleanField('Свободен', default=True,
                               help_text='True - в номере никто не проживает'
                                         'False - на данный момент номер занят')
    visitors = models.ManyToManyField('Visitor', verbose_name='Гости в номере', blank=True)

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.price = set_price(self.category, 'price_room.txt')
        super().save(*args, **kwargs)

    def add_visitor(self, visitor):
        self.visitors.add(visitor)
        self.free = False
        super().save()

    def __str__(self):
        return f'Номер - {self.number}'


class Visitor(models.Model):
    online_client = models.ForeignKey(User, verbose_name='Онлайн аккаунт',
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)
    first_name = models.CharField('Имя пользователя', max_length=255)
    last_name = models.CharField('Фамилия пользователя', max_length=255, db_index=True)
    phone = modelfields.PhoneNumberField('Номер телефона', max_length=255)
    adult = models.BooleanField('Совершенолетие',
                                help_text='True - гость достиг совершенолетия. '
                                          'False - гость не достиг совершенолетия')
    numbers_passport = models.PositiveIntegerField('Номер паспорта')
    number_room = models.ForeignKey(Room, verbose_name='Номер проживания', blank=True,
                                    on_delete=models.PROTECT, null=True, default=None)
    gym = models.ManyToManyField('Gym', verbose_name='Абонимент в спортзал',
                                 related_name='related_visitor', blank=True,
                                 )
    in_hotel = models.BooleanField('Проживает ли на данный момент', default=True)
    check_in_time = models.DateField('Врея заселения', auto_now_add=True)
    eviction_time = models.DateField('Время выселения', null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'Посетител'
        verbose_name_plural = 'Посетители'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if check_in_hotel_visitor(self.number_room):
            self.in_hotel = True
            self.number_room.add_visitor(self)
        super().save(*args, **kwargs)

    def add_gym(self, gym):
        self.gym.add(gym)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.online_client})'


class Gym(models.Model):
    PRICE_GYM = read_price_json_from_txt('price_gym.txt')

    PERIOD_CHOICES = (
        ("1", 'месяц'),
        ("2", '2 месяца'),
        ("3", '3 месяца'),
        ("6", 'пол года'),
        ("12", 'год'),
    )

    visitor = models.OneToOneField(Visitor, verbose_name='Гость', on_delete=models.CASCADE, related_name='related_gum')
    period = models.CharField('Колличество месяцев', max_length=255, choices=PERIOD_CHOICES, blank=False, default=1)
    data_start = models.DateTimeField('Дата покупки', auto_now_add=True)
    data_end = models.DateTimeField('Дата окончания ', default=datetime.datetime.now())
    price = models.CharField('Цена', max_length=255, default='',
                             blank=True,
                             help_text=f'Месяц - {PRICE_GYM["1"]}.\
                                       2 Месяца - {PRICE_GYM["2"]}.\
                                       3 Месяца - {PRICE_GYM["3"]}.\
                                       Пол года - {PRICE_GYM["6"]}.\
                                       Год - {PRICE_GYM["12"]}.')

    class Meta:
        verbose_name = 'Абонимент в зал'
        verbose_name_plural = 'Абонименты в зал'

    def __str__(self):
        return f'Абонимент в зал гостя - {self.visitor.first_name} {self.visitor.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.data_end = set_data_end_gym(int(self.period), self.data_start)
        self.price = set_price(self.period, 'price_gym.txt')
        self.visitor.add_gym(self)
        super().save(*args, **kwargs)
