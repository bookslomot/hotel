from django.urls import path
from django.views.decorators.cache import cache_page

from hotel.views import get_category_room, RoomListAPIView, ApplicationRoomAPIView, \
    BuySubscriptionForGymCreateAPIView, get_rules_room, get_rules_gym,\
    SubscriptionForGymRetrieveAPIView,  ReviewsCreateListViewSets


review_retrieve = ReviewsCreateListViewSets.as_view({
    'get': 'retrieve',
    'patch': 'update'
})

review_create = ReviewsCreateListViewSets.as_view({
    'post': 'create',
})


urlpatterns = [
    # MAIN
    path('categories', cache_page(60)(get_category_room)),
    # RULES
    path('rules-room', cache_page(60)(get_rules_room)),
    path('rules-gym', cache_page(60)(get_rules_gym)),
    # ROOM
    path('room', cache_page(60)(RoomListAPIView.as_view()), name='room-list'),
    path('room/<int:pk>', ApplicationRoomAPIView.as_view(), name='room-retrieve'),
    # GYM
    path('gym_buy', BuySubscriptionForGymCreateAPIView.as_view()),
    path('my_gym', cache_page(30)(SubscriptionForGymRetrieveAPIView.as_view())),
    # RETRIEVE
    path('send_retrieve', review_create, name='review_create'),
    path('my_retrieve', cache_page(60)(review_retrieve), name='review_retrieve'),

]
