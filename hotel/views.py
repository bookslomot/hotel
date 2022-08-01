from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from hotel.models import Room, ApplicationForRoomBron
from hotel.serializer import RoomSerializers
from my_exeptions.exeptions_fun.exeptions_views import base_view
from hotel.services import read_price_json_from_txt


@base_view
@api_view(['GET'])
def get_category_room(request):
    json_data = read_price_json_from_txt('price_room.txt')
    return Response(data=json_data, status=status.HTTP_200_OK)


class CategoriesRoomAPIView(generics.ListAPIView):

    queryset = Room.objects.\
        all().\
        only('number',
             'category',
             'price',
             'number_of_places',
             'free')

    serializer_class = RoomSerializers
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['category', 'number_of_places', 'free']
    ordering_fields = ['number', 'number_of_places']


class ApplicationRoomViewSets(APIView):

    def get(self, *args, **kwargs):
        room = Room.objects.get(pk=self.kwargs['pk'])
        serializer = RoomSerializers(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        room = Room.objects.get(pk=self.kwargs['pk'])
        if not room.free:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ApplicationForRoomBron.objects.create(
            user=request.user,
            room=room
        )
        return Response(status=status.HTTP_201_CREATED)
