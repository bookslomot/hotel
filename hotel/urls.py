from django.urls import path

from hotel.views import get_category_room

urlpatterns = [
    path('categories/', get_category_room),
]