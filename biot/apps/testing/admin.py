from django.contrib import admin

from .models import Quiz, Question, Answer, Choice, Result

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3


""" class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline] """


"""
Начинается блок импорта по схеме Тест -: Вопрос
"""


class QuestionResource(resources.ModelResource):

    def before_import_row(self, row, **kwargs):
        quiz_number = row['quiz']
        Quiz.objects.get_or_create(
            name=quiz_number,
            defaults={'name': quiz_number}
        )

    class Meta:
        model = Question
        fields = ('id', 'quiz', 'name')
        skip_unchanged = True


class QuestionAdmin(ImportExportModelAdmin):
    # inlines = [AnswerInline]
    resource_classes = [QuestionResource]


admin.site.register(Quiz)
admin.site.register(Answer)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Result)
