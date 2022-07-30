from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail

from sendemail.models import MailingLetters, VisitorLetters


@admin.register(MailingLetters)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'is_send')
    search_fields = ('subject',)
    list_filter = ('is_send',)

    def save_related(self, request, form, formsets, change):
        super(EmailAdmin, self).save_related(request, form, formsets, change)
        if form.instance.is_send == 'SEND':
            user_list = []
            for user in form.instance.users.all():
                user_list.append(user.email)
            send_mail(str(form.instance.subject), str(form.instance.message), settings.EMAIL_HOST_USER, user_list)


@admin.register(VisitorLetters)
class CustomerLettersAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', )
    search_fields = ('subject',)










