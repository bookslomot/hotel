from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from hotel.filters import RoomFilter
from hotel.models import Room, ApplicationForRoomBron, Gym, Visitor, Reviews
from hotel.serializer import RoomSerializers, BuySubscriptionForGymSerializers, SubscriptionForGymSerializers, \
    ReviewsSerializers
from my_exeptions.exeptions_fun.exeptions_views import base_view
from hotel.services import read_price_json_from_txt, read_rules


@base_view
@api_view(['GET'])
def get_category_room(request):
    json_data = read_price_json_from_txt('price_room.txt')
    return Response(data=json_data, status=status.HTTP_200_OK)


@base_view
@api_view(['GET'])
def get_rules_room(request):
    data = read_rules('rules_room.txt')
    return Response(data=data, status=status.HTTP_200_OK)


@base_view
@api_view(['GET'])
def get_rules_gym(request):
    data = read_rules('rules_gym.txt')
    return Response(data=data, status=status.HTTP_200_OK)


class RoomListAPIView(generics.ListAPIView):

    queryset = Room.objects.\
        all().\
        only('number',
             'category',
             'price',
             'number_of_places',
             )

    serializer_class = RoomSerializers
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_class = RoomFilter
    ordering_fields = ['number', 'number_of_places']


class ApplicationRoomAPIView(APIView):

    def get(self, *args, **kwargs):
        room = Room.objects.get(pk=self.kwargs['pk'])
        serializer = RoomSerializers(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        room = Room.objects.get(pk=self.kwargs['pk'])
        if room.visitor_set.all().exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ApplicationForRoomBron.objects.create(
            user=request.user,
            room=room
        )
        return Response(status=status.HTTP_201_CREATED)


class BuySubscriptionForGymCreateAPIView(generics.CreateAPIView):

    serializer_class = BuySubscriptionForGymSerializers
    permission_classes = [IsAuthenticated]
    queryset = Gym

    def perform_create(self, serializer):
        visitor = Visitor.objects.get(online_client=self.request.user)
        serializer.save(visitor=visitor)

    def get(self, *args, **kwargs):
        json_data = read_price_json_from_txt('price_gym.txt')
        return Response(data=json_data, status=status.HTTP_200_OK)


class SubscriptionForGymRetrieveAPIView(APIView):

    def get(self, *args, **kwargs):
        gym = Gym.objects.get(visitor__online_client=self.request.user)
        serializers = SubscriptionForGymSerializers(gym)
        return Response(data=serializers.data, status=status.HTTP_200_OK)


class ReviewsCreateListViewSets(viewsets.ModelViewSet):

    serializer_class = ReviewsSerializers
    permission_classes = [IsAuthenticated]
    queryset = Reviews

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = Reviews.objects.filter(owner=request.user)
        serializer = ReviewsSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
