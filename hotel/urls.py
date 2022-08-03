from django.urls import path

from hotel.views import get_category_room, RoomListAPIView, ApplicationRoomAPIView, \
    BuySubscriptionForGymCreateAPIView, get_rules_room, get_rules_gym,\
    SubscriptionForGymRetrieveAPIView,  ReviewsCreateRetrieveViewSets


review_retrieve = ReviewsCreateRetrieveViewSets.as_view({
    'get': 'list',
})

review_create = ReviewsCreateRetrieveViewSets.as_view({
    'post': 'create',
})


urlpatterns = [
    # MAIN
    path('categories/', get_category_room),
    # RULES
    path('rules-room/', get_rules_room),
    path('rules-gym/', get_rules_gym),
    # ROOM
    path('room/', RoomListAPIView.as_view()),
    path('room/<int:pk>', ApplicationRoomAPIView.as_view()),
    # GYM
    path('gym_buy', BuySubscriptionForGymCreateAPIView.as_view()),
    path('my_gym', SubscriptionForGymRetrieveAPIView.as_view()),
    # RETRIEVE
    path('send_retrieve/', review_create, name='review_create'),
    path('my_retrieve/', review_retrieve, name='review_retrieve'),

]
