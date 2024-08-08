from django.conf import settings
from django.db import models

CANDIDATE = 'candidate'
STUDENT = 'student'
MASTER = 'master'

CHOICES_PERSON = (
    (CANDIDATE, 'кандидат'),
    (STUDENT, 'студент'),
    (MASTER, 'выпускник'),
    )


class Group(models.Model):
    grup_number = models.CharField(
        'Номер группы',
        max_length=25,
        help_text='Номер группы',
        unique=True
    )

    program_training = models.TextField(
        'Программа обучения',
        max_length=500,
        help_text='Программа обучения'
    )
    start_date = models.DateField(
        'Дата начала обучения',
        #default='1900-01-01',
        #blank=True,
        null=True
    )

    end_date = models.DateField(
        'Дата окончания обучения',
        #default='1900-01-01',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'Группы обучения'

    def __str__(self):
        return self.grup_number


class Person(models.Model):
    # person = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name='обучающийся',
    #     verbose_name='Обучающийся',
    # )
    uid = models.CharField(
        'UID', max_length=30,
        help_text='UID обучающегося'
    )
    groups = models.ManyToManyField(Group,
                                    related_name='groups',
                                    verbose_name='Номер группы')
    

    status = models.CharField(
        'Статус',
        max_length=15,
        choices=CHOICES_PERSON,
        default=CANDIDATE,
        help_text='Статус обучающегося'
    )
    start_date = models.CharField(
        'Дата начала обучения', blank=True, max_length=15,
        help_text='Дата начала обучения'
    )
    end_date = models.CharField(
        'Дата окончания обучения', blank=True, max_length=15,
        help_text='Дата окончания обучения'
    )

    class Meta:
        verbose_name = 'обучающийся'
        verbose_name_plural = 'Обучающиеся'

    def __str__(self):
        return 'Обучающийся'
