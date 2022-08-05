from datetime import timedelta
import json

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from hotel_DRF.settings import BASE_DIR


def read_price_json_from_txt(path):
    with open(f'{BASE_DIR}\\hotel\\' + path) as f:
        data = f.read()
    js_data = json.loads(data)
    return js_data


def set_price(key_dict, price_name):
    price = read_price_json_from_txt(price_name)
    return str(price[key_dict])


def set_data_end_gym(period: int, data_start):
    days = period * 30
    return data_start + timedelta(days=days)


def check_in_hotel_visitor(number_room):
    if number_room:
        return True
    return False


def accepted_application_for_room(user, room):
    from hotel.models import Visitor
    with transaction.atomic():
        visitor = Visitor.objects.get(
            online_client__email=user.email,
        )
        visitor.in_hotel = True
        visitor.add_room(room)
        email = user.email.split()
        send_mail('Ответ от hotel_DRF',
                  f'Добрый день, {visitor.first_name} {visitor.last_name}, ваша заявка на бронирование комнаты'
                  f'под номером {room} была одобрена. С радостью ожидаем вашего прибытия!',
                  settings.EMAIL_HOST_USER,
                  email)


def read_rules(path):
    with open(f'{BASE_DIR}\\hotel\\' + path, encoding='utf-8') as f:
        data = f.read()
    return data
