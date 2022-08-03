from django.db.models.signals import post_save
from django.dispatch import receiver

from hotel.models import Visitor
from hotel.services import check_in_hotel_visitor


@receiver(post_save, sender=Visitor)
def update_visitor_room(**kwargs):
    instance = kwargs['instance']
    if check_in_hotel_visitor(instance.number_room):
        instance.in_hotel = True
