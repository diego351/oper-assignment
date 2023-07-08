from typing import Any

from app.models import *
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from nested_inline.admin import NestedModelAdmin, NestedStackedInline


class PossibleAnswerInline(NestedStackedInline):
    model = PossibleAnswer
    extra = 1
    fk_name = 'question'
    fields = ('answer', 'is_correct')


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    fk_name = 'quiz'
    inlines = [PossibleAnswerInline]
    fields = ('question',)


class QuizAdmin(NestedModelAdmin):
    model = Quiz
    inlines = [QuestionInline]
    fields = ('name', 'time_limit_minutes', 'creator')
    search_fields = ['name', 'creator__email']
    list_display = ['name', 'creator', 'created_at']


admin.site.register(Quiz, QuizAdmin)


class UserAdmin(admin.ModelAdmin):
    model = User
    search_fields = ['email']


admin.site.register(User, UserAdmin)


class UserAnswerAdmin(admin.ModelAdmin):
    model = UserAnswer

    list_display = ('quiz', 'quiz', 'question', 'answer', 'is_checked')
    fields = ('user_quiz', 'question', 'answer', 'is_checked')

    def user(self, obj):
        return obj.user_quiz.user

    def quiz(self, obj):
        return obj.user_quiz.quiz


admin.site.register(UserAnswer, UserAnswerAdmin)
