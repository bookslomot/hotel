from django.test import TestCase


from hotel.models import Room, Gym, Visitor, Review
from hotel.serializer import RoomSerializers, SubscriptionForGymSerializers, ReviewsSerializers

from user.models import User


class SerializerTestCase(TestCase):

    def test_create_room_RoomSerializers(self):
        """ Сериализация двух комнат с автоматическим параметром - 'price'
                        ('price' зависит от 'category')
        """
        self.room_1 = Room.objects.create(number=1, number_of_places=2)
        self.room_2 = Room.objects.create(number=2, category='Lux', number_of_places=5)

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

    def test_create_gym_SubscriptionForGymSerializers(self):
        """ Сериализация подписки на спортивный абонемент с автоматическим параметром 'price' """

        self.user = User.objects.create(email='test@gmail.com', password='12345678u')
        self.visitor_1 = Visitor.objects.create(online_client=self.user, numbers_passport='12345678')
        self.visitor_2 = Visitor.objects.create(online_client=self.user, numbers_passport='12345678')

        gym_1 = Gym.objects.create(visitor=self.visitor_1, period='3')
        gym_2 = Gym.objects.create(visitor=self.visitor_2, period='6')

        data = SubscriptionForGymSerializers([gym_1, gym_2], many=True).data
        expected_data = [
            {
                'id': gym_1.id,
                'period': '3',
                'visitor': self.visitor_1.id,
                'data_start': data[0]['data_start'],
                'data_end': data[0]['data_end'],
                'price': '2500',
            },
            {
                'id': gym_2.id,
                'period': '6',
                'visitor': self.visitor_2.id,
                'data_start': data[1]['data_start'],
                'data_end': data[1]['data_end'],
                'price': '4000',
            }
        ]
        self.assertEqual(expected_data, data)

    def test_create_review_ReviewsSerializers(self):
        """ Тестирование serializers отзывов """

        self.user = User.objects.create(email='test@gmail.com', password='12345678u')
        review = Review.objects.create(owner=self.user, body='Hello!', rating=4)

        data = ReviewsSerializers(review).data
        expected_data = {
            'id': review.id,
            'body': 'Hello!',
            'rating': '4',
        }
        self.assertEqual(expected_data, data)
