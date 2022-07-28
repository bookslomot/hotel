# Generated by Django 4.0.6 on 2022-07-28 17:47

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(db_index=True, max_length=255, verbose_name='Фамилия пользователя')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='Почта пользователя')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=255, region=None, verbose_name='Номер телефона')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Права администратора')),
                ('is_active', models.BooleanField(default=True, verbose_name='Состояние профиля пользвателя')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания пользователя')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления пользователя')),
                ('avatar', models.ImageField(blank=True, default=None, null=True, upload_to='photo/avatar/%Y/%m/%d', verbose_name='Аватар')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
