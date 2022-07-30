from django.urls import path

from user.views import UserSelfAPIView

urlpatterns = [
    path('me/', UserSelfAPIView.as_view()),
]
