from django.urls import path

from sendemail.views import CreateCustomerLettersAPIView

urlpatterns = [
    path('', CreateCustomerLettersAPIView.as_view())
]
