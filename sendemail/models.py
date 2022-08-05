from django.db import models

from user.models import User


class Latter(models.Model):
    """Абстрактная модель письма"""

    subject = models.CharField('Заголовок', max_length=75)
    message = models.TextField('Тело письма', max_length=1024)
    attach = models.FileField('Файл', upload_to='send_mail/file/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        abstract = True


class MailingLetters(Latter):
    """Модель для хранения всех писем от администрации сайта"""

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
    """Модель для хранения всех писем от пользователей сайта"""

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Писмо от пользователя'
        verbose_name_plural = 'Письма от пользвателей'
