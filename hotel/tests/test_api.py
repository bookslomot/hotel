from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from hotel.models import Room, ApplicationForRoomBron
from hotel.serializer import RoomSerializers


class RoomAPITestCase(APITestCase):

    """ Тестирование API комнат"""

    def setUp(self):
        # Создаются кастомные комнаты
        self.room_1 = Room.objects.create(id=1, number=1, number_of_places=2)
        self.room_2 = Room.objects.create(id=2, number=2, number_of_places=5, category='Lux')
        self.room_3 = Room.objects.create(id=3, number=3, number_of_places=2, category='Studio')
        self.room_4 = Room.objects.create(id=4, number=4, number_of_places=3)
        # Создается зарегистрированный пользователь
        user = get_user_model()
        self.user = user.objects.create_user(email='testmail@gmail.com', password='12345678u')
        self.auth_client = Client()
        self.auth_client.force_login(self.user)

    def test_get_list(self):
        """ Тестирование на корректный вывод списка комнат и статус кода """
        url = reverse('room-list')
        response = self.auth_client.get(url)
        serializer_data = RoomSerializers([self.room_1,
                                           self.room_2,
                                           self.room_3,
                                           self.room_4], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_retrieve(self):
        """ Тестирование на корректный вывод комнаты """
        url = reverse('room-retrieve', args=[2])
        response = self.client.get(url)
        serializer_data = RoomSerializers(self.room_2).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_filter_price(self):
        """ Тестирование фильтрации цены списка комнат """
        url = reverse('room-list')
        response = self.auth_client.get(url, data={'price_max': '10000.00',
                                                   'price_min': '3000.00'})
        serializer_data = RoomSerializers([self.room_1, self.room_4], many=True).data
        print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_filter_number_of_places(self):
        """ Тестирование фильтрации по количеству комнат списка комнат """
        url = reverse('room-list')
        response = self.auth_client.get(url, data={'number_of_places': 5})
        serializer_data = RoomSerializers([self.room_2], many=True).data
        print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
