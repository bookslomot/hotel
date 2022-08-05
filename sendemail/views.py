import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_exeptions.exeptions_fun.exeptions_views import base_view
from sendemail.serializers import LettersSerializer

logger = logging.getLogger(__name__)


@base_view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_latter(request, *args, **kwargs):
    serializer = LettersSerializer(data=request.data)
    with transaction.atomic():
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            subject = str(serializer.data['subject'])
            message = str(serializer.data['message'])
            send_mail(subject, message, request.user.email, [settings.EMAIL_HOST_USER])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
