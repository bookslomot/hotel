from django.urls import path

from hotel.views import get_category_room, CategoriesRoomAPIView, ApplicationRoomViewSets


urlpatterns = [
    path('categories/', get_category_room),
    path('room/', CategoriesRoomAPIView.as_view()),
    path('room/<int:pk>', ApplicationRoomViewSets.as_view()),
]
