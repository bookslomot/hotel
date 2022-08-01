from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_exeptions.exeptions_fun.exeptions_views import base_view
from sendemail.serializers import LettersSerializer


@base_view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_latter(request, *args, **kwargs):
    serializer = LettersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['user'] = request.user
        serializer.save()
        send_mail(str(serializer.data['subject']), str(serializer.data['message']), request.user.email,
                  [settings.EMAIL_HOST_USER])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
