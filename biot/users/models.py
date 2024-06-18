from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import real_age


class CustomUser(AbstractUser):
    # username = models.CharField('Логин', max_length=14, unique=True)
    middle_name = models.CharField('Отчество', max_length=50, blank=True)
    snils = models.CharField('СНИЛС', max_length=14, unique=True, blank=True)
    is_consent = models.BooleanField(
        'Согласие',
        default=False,
        blank=True,
        help_text='Согласие на обработку персональных данных'
    )
    is_verification = models.BooleanField(
        'Верификация',
        default=False,
        blank=True,
        help_text='Верификация пользователя'
    )
    birthday = models.DateField(
        'Дата рождения',
        default='1940-01-01',
        blank=True,
        validators=(real_age,)
    )
    address = models.CharField('Адрес', max_length=200, blank=True)

    # USERNAME_FIELD = 'snils'
    REQUIRED_FIELDS = ['snils']

    def save(self, *args, **kwargs):
        """При импорте нет пароля создается из снилс"""
        if not self.username:
            self.username = self.snils.replace('-', '').replace(' ', '')
        if not self.password:
            self.password = make_password(self.username)
        # if self.snils:
        #     self.is_verification = True
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def __str__(self):
        full_name = self.last_name + ' ' + self.first_name
        return full_name

    # Проверка на уникальность.
    # class Meta:
    #     constraints = (
    #         models.UniqueConstraint(
    #             fields=('first_name', 'last_name', 'birthday'),
    #             name='Unique person constraint',
    #         ),
    #     )
