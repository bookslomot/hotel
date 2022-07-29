from django.db.models.signals import pre_save, pre_init
from django.dispatch import receiver

from hotel.models import Visitor, Gym, Room


# @receiver(pre_init, sender=Visitor)
# def delete_visitor_in_room(**kwargs):
#     print(kwargs['args'])



