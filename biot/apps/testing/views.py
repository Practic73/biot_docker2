from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Quiz, Question, Answer, Choice, Result
from .utils import paginateObjects


@login_required
def quizzes(request):
    # profile = request.user.profile
    quizzes = Quiz.objects.all()
    custom_range, quizzes = paginateObjects(request, quizzes, 3)
    context = {
        'quizzes': quizzes,
    }
    return render(request, 'testing/quizzes.html', context)


@login_required
def display_quiz(request, quiz_name):
    quiz = get_object_or_404(Quiz, pk=quiz_name)
    question = quiz.question_set.first()
    return redirect(
        reverse(
            'testing:display_question',
            kwargs={'quiz_name': quiz_name, 'question_id': question.pk}
        )
    )


@login_required
def display_question(request, quiz_name, question_id):
    # profile = request.user.profile
    quiz = get_object_or_404(Quiz, pk=quiz_name)
    questions = quiz.question_set.all()
    current_question, next_question = None, None
    for ind, question in enumerate(questions):
        if question.pk == question_id:
            current_question = question
            if ind != len(questions) - 1:
                next_question = questions[ind + 1]
    context = {
        'quiz': quiz,
        'question': current_question,
        'next_question': next_question,
        # 'profile': profile
    }
    return render(request, 'testing/display.html', context)


@login_required
def grade_question(request, quiz_name, question_id):
    question = get_object_or_404(Question, pk=question_id)
    quiz = get_object_or_404(Quiz, pk=quiz_name)
    can_answer = question.user_can_answer(request.user)
    try:
        if not can_answer:
            return render(
                request,
                'testing/partial.html',
                {
                    'question': question,
                    'error_message': 'Вы уже отвечали на этот вопрос.'
                }
            )

        if question.qtype == 'single':
            correct_answer = question.get_answers()
            user_answer = question.answer_set.get(pk=request.POST['answer'])
            choice = Choice(
                user=request.user,
                question=question, answer=user_answer)
            choice.save()
            is_correct = correct_answer == user_answer
            result, created = Result.objects.get_or_create(
                user=request.user,
                quiz=quiz
            )
            if is_correct is True:
                result.correct = F('correct') + 1
            else:
                result.wrong = F('wrong') + 1
            result.save()

        elif question.qtype == 'multiple':
            correct_answer = question.get_answers()
            answers_ids = request.POST.getlist('answer')
            user_answers = []
            if answers_ids:
                for answer_id in answers_ids:
                    user_answer = Answer.objects.get(pk=answer_id)
                    user_answers.append(user_answer.name)
                    choice = Choice(
                        user=request.user,
                        question=question, answer=user_answer)
                    choice.save()
                is_correct = correct_answer == user_answers
                result, created = Result.objects.get_or_create(
                    user=request.user,
                    quiz=quiz
                )
                if is_correct is True:
                    result.correct = F('correct') + 1
                else:
                    result.wrong = F('wrong') + 1
                result.save()
    except BaseException:
        return render(
            request, 'testing/partial.html',
            {'question': question})
    return render(
        request,
        'testing/partial.html',
        {
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'question': question
        }
    )


@login_required
def quiz_results(request, quiz_name):
    # profile = request.user.profile
    quiz = get_object_or_404(Quiz, pk=quiz_name)
    questions = quiz.question_set.all()
    results = Result.objects.filter(
        user=request.user,
        quiz=quiz
    ).values()
    correct = [i['correct'] for i in results][0]
    wrong = [i['wrong'] for i in results][0]
    context = {
        'quiz': quiz,
        # 'profile': profile,
        'correct': correct,
        'wrong': wrong,
        'number': len(questions),
        'skipped': len(questions) - (correct + wrong)
    }
    return render(
        request,
        'testing/results.html', context
    )
