from hotel.models import Room
from django_filters import rest_framework as filters


class RoomFilter(filters.FilterSet):
    price = filters.RangeFilter()

    class Meta:
        model = Room
        fields = ['price', 'category', 'number_of_places']
