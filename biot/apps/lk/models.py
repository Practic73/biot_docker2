from django.conf import settings
from django.db import models

CANDIDATE = 'candidate'
STUDENT = 'student'
MASTER = 'master'

CHOICES_PERSON = (
    (CANDIDATE, 'Кандидат'),
    (STUDENT, 'Обучающийся'),
    (MASTER, 'Выпускник'),
    )


class Group(models.Model):
    group_number = models.CharField(
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
        null=True
    )

    end_date = models.DateField(
        'Дата окончания обучения',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'Группы обучения'

    def __str__(self):
        return self.group_number


class Person(models.Model):
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='обучающийся',
        verbose_name='Обучающийся',
    )
    uid = models.CharField(
        'UID', max_length=50,
        help_text='UID обучающегося'
    )
    group = models.ForeignKey(Group,
                              on_delete=models.PROTECT,
                              related_name='group',
                              verbose_name='Текущая группа')

    previous_groups = models.CharField(
        'Предыдущие группы', max_length=30,
        blank=True,
        help_text='Предыдущие группы'
    )

    status = models.CharField(
        'Статус',
        max_length=15,
        choices=CHOICES_PERSON,
        default=CANDIDATE,
        help_text='Статус обучающегося'
    )

    start_date_person = models.DateField(
        'Дата начала обучения',
        null=True
    )

    end_date_person = models.DateField(
        'Дата окончания обучения',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        """Дата начала обучения"""
        if self.start_date_person and not self.end_date_person:
            self.status = STUDENT
        elif self.start_date_person and self.end_date_person:
            self.status = MASTER
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'обучающийся'
        verbose_name_plural = 'Обучающиеся'

    def __str__(self):
        return 'Обучающийся'