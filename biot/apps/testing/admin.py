from django.contrib import admin

from .models import Quiz, Question, Answer, Choice, Result

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 3


""" class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline] """


"""
Начинается блок импорта по схеме Тест -: Вопрос
"""


class QuestionResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        quiz_number = row['quiz']
        quiz = Quiz.objects.get_or_create(
            name=quiz_number,
            defaults={'name': quiz_number}
        )

        question_name = Question.objects.get_or_create(
            name=row['name'],
            quiz=quiz,
        )
        if question_name:
            answer = row['answer']
            is_correct = True if row['is_correct'] == '+' else False
            Answer.objects.get_or_create(
                name=answer,
                is_correct=is_correct,
                question=self.instance,
                defaults={'name': answer}
            )

    def after_save_instance(self, instance, using_transactions, dry_run):
        self.instance = instance
        return super().after_save_instance(
            instance,
            using_transactions,
            dry_run
        )

    def after_import_row(self, row, row_result, row_number=None, **kwargs):
        answer = row['answer']
        is_correct = True if row['is_correct'] == '+' else False
        Answer.objects.get_or_create(
            name=answer,
            is_correct=is_correct,
            question=self.instance,
            defaults={'name': answer}
        )

    class Meta:
        model = Question
        fields = ('id', 'quiz', 'name')
        skip_unchanged = False
        report_skipped = False


class QuestionAdmin(ImportExportModelAdmin):
    inlines = [AnswerInline]
    resource_classes = [QuestionResource]


class QuizAdmin(ImportExportModelAdmin):
    inlines = [QuestionInLine]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Answer)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Result)
