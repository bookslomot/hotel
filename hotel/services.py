from datetime import timedelta


PRICE_GYM = {1: 1000,
             2: 1800,
             3: 2500,
             6: 4000,
             12: 8000}

PRICE_ROOM = {'Suite': 30000,
              'Apartment': 22000,
              'Lux': 15000,
              'Junior Suite': 11000,
              'Studio': 8000,
              'Standard': 5000}


def set_price_gym(period):
    return str(PRICE_GYM[period])


def set_price_room(category):
    return str(PRICE_ROOM[category])


def set_data_end(period, data_start):
    days = period * 30
    return data_start + timedelta(days=days)

