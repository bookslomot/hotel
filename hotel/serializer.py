from rest_framework import serializers

from hotel.models import Room, Gym, Review


class RoomSerializers(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('id', 'number', 'category', 'price', 'number_of_places',)


class BuySubscriptionForGymSerializers(serializers.ModelSerializer):

    class Meta:
        model = Gym
        fields = ('period',)


class SubscriptionForGymSerializers(serializers.ModelSerializer):

    class Meta:
        model = Gym
        fields = ('id', 'period', 'visitor', 'data_start', 'data_end', 'price',)


class ReviewsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'body', 'rating',)
