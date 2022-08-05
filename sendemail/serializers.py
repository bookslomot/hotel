from rest_framework import serializers

from sendemail.models import VisitorLetters
from user.models import User


class ReviewUserInVisitorLetters(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name')


class LettersSerializer(serializers.ModelSerializer):
    """Сериализация писем пользователей """

    user = ReviewUserInVisitorLetters(read_only=True)

    class Meta:
        model = VisitorLetters
        fields = ('subject', 'message', 'user', 'attach')
