from rest_framework import serializers

from hotel.models import Room


class RoomSerializers(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('id', 'number', 'category', 'price', 'number_of_places',)
