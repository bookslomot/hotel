from django.db import models
from phonenumber_field import modelfields

from hotel.services import set_data_end_gym, set_price, read_price_json_from_txt, accepted_application_for_room
from user.models import User


class Room(models.Model):
    CATEGORY_CHOICES = (
        ('Suite', 'Сюит'),
        ('Apartment', 'Апартамент '),
        ('Lux', 'Люкс '),
        ('Junior Suite', 'Джуниор Сюит'),
        ('Studio', 'Студия'),
        ('Standard', 'стандарт'),

    )

    number = models.PositiveIntegerField('Порядковый номер')
    category = models.CharField('Категория номера',
                                choices=CATEGORY_CHOICES,
                                max_length=255,
                                blank=False,
                                default='Standard')
    price = models.DecimalField('Цена за ночь', max_digits=8, decimal_places=2, default=1, blank=True)
    number_of_places = models.PositiveSmallIntegerField('Колличество мест')

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.price = set_price(self.category, 'price_room.txt')
        super().save(update_fields=['price'])

    def __str__(self):
        return f'Номер - {self.number}'


class Visitor(models.Model):
    online_client = models.ForeignKey(User, verbose_name='Онлайн аккаунт',
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)
    first_name = models.CharField('Имя пользователя', max_length=255,)
    last_name = models.CharField('Фамилия пользователя', max_length=255,)
    phone = modelfields.PhoneNumberField('Номер телефона', max_length=255,)
    adult = models.BooleanField('Совершенолетие',
                                help_text='True - гость достиг совершенолетия. '
                                          'False - гость не достиг совершенолетия',
                                default=False)
    numbers_passport = models.PositiveBigIntegerField('Номер паспорта',)
    number_room = models.ForeignKey(Room, verbose_name='Номер проживания', blank=True,
                                    on_delete=models.PROTECT, null=True, default=None)
    gym = models.ManyToManyField('Gym', verbose_name='Абонимент в спортзал',
                                 related_name='related_visitor', blank=True,)
    in_hotel = models.BooleanField('Проживает ли на данный момент', default=True)
    check_in_time = models.DateField('Врея заселения', auto_now_add=True)
    eviction_time = models.DateField('Время выселения', null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'Посетител'
        verbose_name_plural = 'Посетители'

    def add_gym(self, gym):
        self.gym.add(gym)

    def add_room(self, room):
        self.number_room = room
        self.save()

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
    data_end = models.DateTimeField('Дата окончания ', blank=True, null=True)
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

    def save(self, *args, **kwargs, ):
        super(Gym, self).save()
        self.data_end = set_data_end_gym(int(self.period), self.data_start)
        self.price = set_price(self.period, 'price_gym.txt')
        self.visitor.add_gym(self)
        super(Gym, self).save(update_fields=['data_end', 'price'])


class Review(models.Model):
    RATING_1_5 = (
        ('1', 'terribly'),
        ('2', 'bad'),
        ('3', 'ok'),
        ('4', 'good'),
        ('5', 'amazing')
    )

    owner = models.OneToOneField(User, verbose_name='Автор отзыва', on_delete=models.PROTECT,)
    body = models.TextField('Тело текста отзыва', max_length=1024,)
    file = models.FileField('Прикрепленный файл к отзыву', upload_to='reviews/%Y/%m/%d/', null=True, blank=True,)
    created_at = models.DateTimeField('Время создания отзыва', auto_now_add=True,)
    updated_at = models.DateTimeField('Время последнего обновления отзыва', auto_now=True,)
    active = models.BooleanField('Состояние отзыва', default=True,)
    rating = models.CharField('Рейтинг отеля', max_length=25, choices=RATING_1_5, null=True, blank=True,)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв от - {self.owner.email}'


class ApplicationForRoomBron(models.Model):

    STATUS_APPLICATION = (
        ('True', 'Одобрена'),
        ('False', 'Откланенна'),
        ('in progress', 'В процессе обработки')
    )

    user = models.ForeignKey(User, verbose_name='Владелец заявки на бронь', on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, verbose_name='Желаемая комната на бронь', on_delete=models.SET_NULL, null=True)
    status = models.CharField('Статус заявки', choices=STATUS_APPLICATION, max_length=255, blank=True,
                              default=STATUS_APPLICATION[2][0])

    class Meta:
        verbose_name = 'Заявка на бронь комнаты'
        verbose_name_plural = 'Заявки на бронь комнаты'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'True':
            accepted_application_for_room(self.user, self.room)

    def __str__(self):
        return f'Заявка {self.user} на комнату {self.room}'
