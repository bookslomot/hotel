from datetime import timedelta
import json


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


