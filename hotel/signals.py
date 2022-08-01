# from django.conf import settings
# from django.core.mail import send_mail
# from django.db import transaction
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from hotel.models import Visitor
# from user.models import User
#
#
# @receiver(post_save, sender=User)
# def create_visitor(**kwargs):
#     instance = kwargs['instance']
#     print(instance.first_name, instance.last_name, instance.phone + 'fewfwfwfwfwfwfwfwfwefwfwfwefw')
#     Visitor.objects.create(
#         first_name=instance.first_name,
#         last_name=instance.last_name,
#         phone=instance.phone,
#     )
#     email = instance.email.split()
#     send_mail('Уведомление от hotel_DRF',
#               'Добрый день, на ваш аккаунт был оформлен гость в нашем отеле,'
#               'если вы не делали этого, то .....',
#               settings.EMAIL_HOST_USER,
#               email
#
#          )







