from unittest import TestCase

from user.models import User


class UserModerCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='user4@gmail.com',
            password='12345678u'
        )

    # def test_email(self):
    #     email = self.user.email
    #     self.assertEqual(email, 'user2@gmail.com')

    # def test_password(self):
    #     password = self.user.password
    #     self.assertEqual(password, '12345678u')
