from django.conf import settings
from django.db import models


class ReestrOt(models.Model):
    reestr_number = models.CharField(
        'Номер реестра',
        max_length=25,
        help_text='Номер в реестре',
        unique=True
    )
    reestr_date = models.CharField(
        'Дата реестра',
        max_length=15,
        help_text='Дата внесения в реестр'
    )
    reestr_id_packet = models.CharField(
        'ID пакета',
        max_length=15,
        help_text='ID пакета в реестре'
    )
    is_sistem = models.BooleanField(
        'В системе',
        default=False,
        blank=True,
        help_text='Сдача экзамена в системе ЕИСОТ'
    )
    prot_number = models.CharField(
        'Номер протокола',
        max_length=15,
        help_text='Номер протокола'
    )
    prot_date = models.CharField(
        'Дата протокола', blank=True, max_length=15,
        help_text='Дата проверки знаний'
    )

    program = models.TextField(
        'Программа',
        max_length=256,
        help_text='Программа обучения'
    )

    result = models.CharField(
        'Результат',
        max_length=25,
        help_text='Результат проверки знаний'
    )
    employer = models.CharField(
        'Работодатель', blank=True,
        max_length=100,
        help_text='Наименование работодателя',
    )
    employer_inn = models.CharField(
        'ИНН работодателя', max_length=25,
        help_text='ИНН работодателя',
    )
    position_at_work = models.CharField(
        'Должность',
        blank=True,
        max_length=100,
        help_text='Должность',
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='работник',
        verbose_name='Работник',
    )

    class Meta:
        verbose_name = 'реестр'
        verbose_name_plural = 'Выписка из реестра ЕИСОТ'

    def __str__(self):
        return self.reestr_number
