from django.db.models.signals import post_init
from django.dispatch import receiver

from hotel.models import Visitor
from hotel.services import check_in_hotel_visitor


@receiver(post_init, sender=Visitor)
def update_visitor_room(**kwargs):
    instance = kwargs['instance']
    instance.in_hotel = check_in_hotel_visitor(instance.number_room)
