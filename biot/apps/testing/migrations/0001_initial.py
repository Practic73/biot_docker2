# Generated by Django 4.2.8 on 2024-08-01 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Верный ответ')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False, unique=True, verbose_name='Название теста')),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='Опубликован')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
                'ordering': ['published'],
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.IntegerField(default=0, verbose_name='Кол-во верных ответов')),
                ('wrong', models.IntegerField(default=0, verbose_name='Кол-во неверных ответов')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.quiz', verbose_name='Тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Результат',
                'verbose_name_plural': 'Результаты',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350, verbose_name='Название')),
                ('qtype', models.CharField(choices=[('single', 'Single'), ('multiple', 'Multiple')], default='single', max_length=8)),
                ('explanation', models.CharField(default=' - ', max_length=550, verbose_name='Пояснение')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.quiz', verbose_name='Тест')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.answer', verbose_name='Ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.question', verbose_name='Тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Ответ пользователя',
                'verbose_name_plural': 'Ответы пользователя',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.question', verbose_name='Вопрос'),
        ),
    ]
