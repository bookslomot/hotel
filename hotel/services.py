from datetime import timedelta
import json

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction


def read_price_json_from_txt(path):
    with open('A:\\Django\\hotel_DRF\\hotel\\' + path) as f:
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


def accepted_application_for_room(email, room):
    from hotel.models import Visitor
    with transaction.atomic():
        visitor = Visitor.objects.get(online_client__email=email)
        room.add_visitor(visitor)
        visitor.in_hotel = True
        visitor.add_room(room)
        email = email.split()
        send_mail('Ответ от hotel_DRF',
                  f'Добрый день, {visitor.first_name} {visitor.last_name}, ваша заявка на бронирование комнаты'
                  f'под номером {room} была одобрена. С радостью ожидаем вашего прибытия!',
                  settings.EMAIL_HOST_USER,
                  email)
