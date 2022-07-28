from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field import modelfields


class UserManager(BaseUserManager):

    def create_user(self, email, password):

        if email is None:
            raise TypeError('User must have a email')
        if password is None:
            raise TypeError('User must have a password')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField('Имя пользователя', max_length=255)
    last_name = models.CharField('Фамилия пользователя', max_length=255, db_index=True)
    email = models.EmailField('Почта пользователя', max_length=255, unique=True, db_index=True)
    phone = modelfields.PhoneNumberField('Номер телефона', max_length=255)
    is_staff = models.BooleanField('Права администратора', default=False)
    is_active = models.BooleanField('Состояние профиля пользвателя', default=True)
    created_at = models.DateTimeField('Время создания пользователя', auto_now_add=True)
    updated_at = models.DateTimeField('Дата последнего обновления пользователя', auto_now=True)
    avatar = models.ImageField('Аватар', upload_to='photo/avatar/%Y/%m/%d',
                               blank=True, null=True, default=None)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.first_name} {self.last_name} ({self.email})'

    def get_full_name(self):
        return f'{self.first_name}  {self.last_name}'
