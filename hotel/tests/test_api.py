import json

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from hotel.models import Room, Gym, Visitor, Review, ApplicationForRoomBron
from hotel.serializer import RoomSerializers, SubscriptionForGymSerializers, ReviewsSerializers
from user.models import User


class HotelAPITestCase(APITestCase):

    def setUp(self):
        # Создаются комнаты

        self.room_1 = Room.objects.create(id=1, number=1, number_of_places=2)
        self.room_2 = Room.objects.create(id=2, number=2, number_of_places=5, category='Lux')
        self.room_3 = Room.objects.create(id=3, number=3, number_of_places=2, category='Studio')
        self.room_4 = Room.objects.create(id=4, number=4, number_of_places=3)
        # Создается зарегистрированный пользователь

        user = get_user_model()
        self.user = user.objects.create(email='testmail@gmail.com', password='12345678u')
        self.auth_client = Client()
        self.auth_client.force_login(self.user)

    def test_get_list_room(self):
        """ Тестирование на корректный вывод списка комнат и статус кода """

        url = reverse('room-list')
        response = self.auth_client.get(url)
        serializer_data = RoomSerializers([self.room_1,
                                           self.room_2,
                                           self.room_3,
                                           self.room_4], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_retrieve_room(self):
        """ Тестирование на корректный вывод комнаты """

        url = reverse('room-retrieve', args=[self.room_2.pk])
        response = self.client.get(url)
        serializer_data = RoomSerializers(self.room_2).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_filter_price_room(self):
        """ Тестирование фильтрации цены списка комнат """

        url = reverse('room-list')
        response = self.auth_client.get(url, data={'price_max': '10000.00',
                                                   'price_min': '3000.00'})
        serializer_data = RoomSerializers([self.room_1, self.room_4], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_filter_number_of_places_room(self):
        """ Тестирование фильтрации по количеству комнат списка комнат """

        url = reverse('room-list')
        response = self.auth_client.get(url, data={'number_of_places': 5})
        serializer_data = RoomSerializers([self.room_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create_application_room(self):
        """ Тестирование создания заявки"""
        self.assertEqual(0, ApplicationForRoomBron.objects.count())
        url = reverse('room-retrieve', args=[2])
        response = self.auth_client.post(url)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, ApplicationForRoomBron.objects.count())
        self.assertEqual(True, bool(ApplicationForRoomBron.objects.get(room=self.room_2)))

    def test_get_gym(self):
        """ Тестирование просмотра абонемента """

        visitor = Visitor.objects.get_or_create(online_client=self.user, numbers_passport='12345678')[0]

        self.gym = Gym.objects.create(visitor=visitor, period='3')
        url = reverse('my-gym')
        response = self.auth_client.get(url)
        serializer_data = SubscriptionForGymSerializers(self.gym).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_post_buy_gym(self):
        """ Тестирование покупки абонемента в зал """
        visitor = Visitor.objects.get_or_create(online_client=self.user, numbers_passport='12345678')[0]

        self.assertEqual(0, Gym.objects.all().count())
        url = reverse('buy-gym')
        data = {
            'period': '3',
            'visitor': visitor.id,
        }
        json_data = json.dumps(data)
        response = self.auth_client.post(url, data=json_data, content_type='application/json')
        gym_price_dict = Gym.objects.values('price').first()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Gym.objects.all().count())
        self.assertEqual('2500', gym_price_dict['price'])

    def test_create_review(self):
        """ Тестирование создания отзыва """

        self.assertEqual(0, Review.objects.all().count())
        url = reverse('review_create')
        data = {
            'body': 'Hello',
            'rating': '4'
        }
        json_data = json.dumps(data)
        response = self.auth_client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Review.objects.all().count())

    def test_get_retrieve_review(self):
        """ Тестирование на корректный вывод отзыва """

        review = Review.objects.create(owner=self.user, body='Hello', rating='3')
        url = reverse('review_retrieve')
        response = self.auth_client.get(url)
        serializer_data = ReviewsSerializers([review], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
