from django.db import models

from user.models import User


class Latter(models.Model):

    subject = models.CharField(max_length=75)
    message = models.TextField(max_length=1024)

    class Meta:
        abstract = True


class MailingLetters(Latter):

    send = (
        ('SEND', 'Отправить'),
        ('Draft', 'Черновик'),
    )

    users = models.ManyToManyField(User, verbose_name='Отправка пользователям')
    is_send = models.CharField('Состояние письма', choices=send, max_length=255,
                               help_text='Отправлять или в черновик')

    class Meta:
        verbose_name = 'Писмьо админа'
        verbose_name_plural = 'Письма админа'


class VisitorLetters(Latter):

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Писмо от пользователя'
        verbose_name_plural = 'Письма от пользвателей'
