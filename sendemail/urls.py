from django.urls import path

from sendemail.views import post_latter

urlpatterns = [
    path('', post_latter)
]
