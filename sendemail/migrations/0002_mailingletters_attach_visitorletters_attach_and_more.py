# Generated by Django 4.0.6 on 2022-08-05 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendemail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingletters',
            name='attach',
            field=models.FileField(blank=True, null=True, upload_to='send_mail/file/%Y/%m/%d/', verbose_name='Файл'),
        ),
        migrations.AddField(
            model_name='visitorletters',
            name='attach',
            field=models.FileField(blank=True, null=True, upload_to='send_mail/file/%Y/%m/%d/', verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='mailingletters',
            name='message',
            field=models.TextField(max_length=1024, verbose_name='Тело письма'),
        ),
        migrations.AlterField(
            model_name='mailingletters',
            name='subject',
            field=models.CharField(max_length=75, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='visitorletters',
            name='message',
            field=models.TextField(max_length=1024, verbose_name='Тело письма'),
        ),
        migrations.AlterField(
            model_name='visitorletters',
            name='subject',
            field=models.CharField(max_length=75, verbose_name='Заголовок'),
        ),
    ]