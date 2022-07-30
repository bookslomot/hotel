from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from my_exeptions.exeptions_fun.exeptions_views import base_view
from hotel.services import read_price_json_from_txt


@base_view
@api_view(['GET'])
def get_category_room(request):
    json_data = read_price_json_from_txt('price_room.txt')
    return Response(data=json_data, status=status.HTTP_200_OK)

