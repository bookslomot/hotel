# Generated by Django 4.0.6 on 2022-08-05 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendemail', '0003_alter_mailingletters_attach_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingletters',
            name='attach',
            field=models.FileField(blank=True, null=True, upload_to='send_mail/file/%Y/%m/%d/', verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='visitorletters',
            name='attach',
            field=models.FileField(blank=True, null=True, upload_to='send_mail/file/%Y/%m/%d/', verbose_name='Файл'),
        ),
    ]
