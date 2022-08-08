import logging
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from hotel.filters import RoomFilter
from hotel.models import Room, ApplicationForRoomBron, Gym, Visitor, Reviews
from hotel.permissions import IsOwner
from hotel.serializer import RoomSerializers, BuySubscriptionForGymSerializers, SubscriptionForGymSerializers, \
    ReviewsSerializers
from my_exeptions.exeptions_class.exeptions_views import BaseView
from my_exeptions.exeptions_fun.exeptions_views import base_view
from hotel.services import read_price_json_from_txt, read_rules

logger = logging.getLogger(__name__)


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


class RoomListAPIView(generics.ListAPIView, BaseView):

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


class ApplicationRoomAPIView(APIView, BaseView):

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


class BuySubscriptionForGymCreateAPIView(generics.CreateAPIView, BaseView):

    serializer_class = BuySubscriptionForGymSerializers
    permission_classes = [IsAuthenticated]
    queryset = Gym

    def perform_create(self, serializer):
        visitor = Visitor.objects.get(online_client=self.request.user)
        serializer.save(visitor=visitor)

    def get(self, *args, **kwargs):
        json_data = read_price_json_from_txt('price_gym.txt')
        return Response(data=json_data, status=status.HTTP_200_OK)


class SubscriptionForGymRetrieveAPIView(APIView, BaseView):

    def get(self, *args, **kwargs):
        try:
            gym = Gym.objects.get(visitor__online_client=self.request.user)
            serializers = SubscriptionForGymSerializers(gym)
            return Response(data=serializers.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ReviewsCreateListViewSets(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                GenericViewSet):

    serializer_class = ReviewsSerializers
    permission_classes = [IsAuthenticated]
    queryset = Reviews

    def get_permissions(self):
        if self.action in ['retrieve']:
            permission_classes = [IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        queryset = Reviews.objects.\
            filter(owner=request.user).\
            only('body',
                 'rating'
                 )
        serializer = ReviewsSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = Reviews.objects.get(owner=request.user)
        serializer = ReviewsSerializers(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
