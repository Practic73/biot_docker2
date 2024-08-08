from django.urls import path

from . import views

app_name = 'testing'

urlpatterns = [
    path('quizzes/', views.quizzes, name='quizzes'),
    path('<str:quiz_name>/', views.display_quiz, name='display_quiz'),
    path(
        '<str:quiz_name>/questions/<int:question_id>',
        views.display_question,
        name='display_question'
    ),
    path(
        '<str:quiz_name>/questions/<int:question_id>/grade/',
        views.grade_question,
        name='grade_question'
    ),
    path(
        'results/<str:quiz_name>/',
        views.quiz_results,
        name='quiz_results'
    ),
]
