from django.test import TestCase

from django.db.models import PositiveSmallIntegerField

from hotel.models import Room
from hotel.serializer import RoomSerializers


class RoomSerializerTestCase(TestCase):

    """ Тестирование serializers комнат """

    def setUp(self):
        # Создаются две кастомные комнаты
        self.room_1 = Room.objects.create(number=1, number_of_places=2)
        self.room_2 = Room.objects.create(number=2, category='Lux', number_of_places=5)

    def test_create_two_room(self):
        """ Сериализация двух комнат с автоматическим параметром - 'price'
                        ('price' зависит от 'category')
        """
        data = RoomSerializers([self.room_1, self.room_2], many=True).data
        expected_data = [
            {
                'id': self.room_1.id,
                'number': 1,
                'category': 'Standard',
                'price': '5000.00',
                'number_of_places': 2,
            },
            {
                'id': self.room_2.id,
                'number': 2,
                'category': 'Lux',
                'price': '15000.00',
                'number_of_places': 5,
            }
        ]
        self.assertEqual(expected_data, data)
