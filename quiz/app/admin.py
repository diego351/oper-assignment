import csv
from typing import Any

from app.models import *
from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import Quiz


class PossibleAnswerInline(NestedStackedInline):
    model = PossibleAnswer
    extra = 1
    fk_name = 'question'
    fields = ('answer', 'is_correct')


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    fk_name = 'quiz'
    inlines = (PossibleAnswerInline,)
    fields = ('question',)


def export_daily_report(modeladmin, request, queryset):
    # Query the database to get the count of quizzes created per day
    daily_counts = (
        Quiz.objects.annotate(created_date=TruncDate('created_at')).values('created_date').annotate(count=Count('id'))
    )

    rows = ('Date', 'Number of Quizzes')
    for count in daily_counts:
        rows.append((count('created_date').strftime('%Y-%m-%d'), count('count')))

    # Generate the CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="daily_report.csv"'

    writer = csv.writer(response)
    for row in rows:
        writer.writerow(row)

    return response
    # TODO: add streaming CSV to handle very large tables


export_daily_report.short_description = 'Export Daily Report'


class QuizAdmin(NestedModelAdmin):
    model = Quiz
    inlines = (QuestionInline,)
    fields = ('id', 'name', 'time_limit', 'creator')
    search_fields = ('id', 'name', 'creator__email')
    list_display = ('id', 'name', 'creator', 'created_at')
    actions = (export_daily_report,)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "creator":
            kwargs["queryset"] = User.objects.filter(user_type=User.UserType.CREATOR)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ('id', 'email', 'user_type')
    search_fields = ('id', 'email', 'user_type')
    list_display = ('id', 'email', 'user_type')
    list_filter = ('user_type',)


class UserAnswerAdmin(admin.ModelAdmin):
    model = UserAnswer

    list_display = ('id', 'user', 'user_quiz', 'question', 'answer', 'is_checked')
    fields = ('id', 'user', 'user_quiz', 'question', 'answer', 'is_checked')

    def user(self, obj):
        return obj.user_quiz.user

    def quiz(self, obj):
        return obj.user_quiz.quiz


class UserQuizAdmin(admin.ModelAdmin):
    model = UserQuiz

    list_display = ('id', 'user', 'quiz', 'started_at', 'finished_at')
    fields = ('id', 'user', 'quiz', 'started_at', 'finished_at', 'results_sent')


admin.site.register(User, UserAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(UserQuiz, UserQuizAdmin)
admin.site.register(Quiz, QuizAdmin)
