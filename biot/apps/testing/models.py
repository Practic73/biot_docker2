from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Quiz(models.Model):
    name = models.CharField(
        verbose_name='Название теста',
        max_length=120,
        unique=True,
        primary_key=True,
    )
    published = models.DateTimeField(verbose_name='Опубликован',
                                     auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['published']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    class qtype(models.TextChoices):
        single = 'single'
        multiple = 'multiple'

    name = models.CharField(
        verbose_name='Название',
        max_length=350,
        unique=True,
    )
    qtype = models.CharField(
        max_length=8,
        choices=qtype.choices,
        default=qtype.single
    )
    quiz = models.ForeignKey(
        Quiz,
        verbose_name='Тест',
        on_delete=models.CASCADE
    )
    explanation = models.CharField(
        verbose_name='Пояснение',
        max_length=550,
        default=' - ')

    def get_answers(self):
        if self.qtype == 'single':
            return self.answer_set.filter(is_correct=True).first()
        else:
            qs = self.answer_set.filter(is_correct=True).values()
            return [i.get('name') for i in qs]

    def user_can_answer(self, user):
        user_choices = user.choice_set.all()
        done = user_choices.filter(question=self)
        print(done)
        if done.exists():
            return False
        return True

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name='Название', max_length=200)
    is_correct = models.BooleanField(
        verbose_name='Верный ответ',
        default=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Choice(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        verbose_name='Тест',
        on_delete=models.CASCADE
    )
    answer = models.ForeignKey(
        Answer,
        verbose_name='Ответ',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователя'


class Result(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        verbose_name='Тест',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    correct = models.IntegerField(
        verbose_name='Кол-во верных ответов',
        default=0
    )
    wrong = models.IntegerField(
        verbose_name='Кол-во неверных ответов',
        default=0
    )

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
