from django.urls import path
from django.views.decorators.cache import cache_page

from hotel import views


review_retrieve = views.ReviewsCreateListViewSets.as_view({
    'get': 'retrieve',
    'patch': 'update'
})

review_create = views.ReviewsCreateListViewSets.as_view({
    'post': 'create',
})


urlpatterns = [
    # MAIN
    path('categories', cache_page(60)(views.get_category_room)),
    # RULES
    path('rules-room', cache_page(60)(views.get_rules_room)),
    path('rules-gym', cache_page(60)(views.get_rules_gym)),
    # ROOM
    path('room', cache_page(60)(views.RoomListAPIView.as_view()), name='room-list'),
    path('room/<int:pk>', views.ApplicationRoomAPIView.as_view(), name='room-retrieve'),
    # GYM
    path('gym_buy', views.BuySubscriptionForGymCreateAPIView.as_view()),
    path('my_gym', cache_page(30)(views.SubscriptionForGymRetrieveAPIView.as_view())),
    # RETRIEVE
    path('send_retrieve', review_create, name='review_create'),
    path('my_retrieve', cache_page(60)(review_retrieve), name='review_retrieve'),

]
