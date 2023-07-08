from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    BooleanField,
    DateTimeField,
    EmailField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    TextField,
)
from django.utils import timezone

__all__ = ('Quiz', 'Question', 'User', 'UserQuiz', 'PossibleAnswer', 'UserAnswer')


class BaseModel(Model):
    updated_at = DateTimeField(null=True)
    created_at = DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()

        return super().save()

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    pass

    def __str__(self):
        return self.email


class Quiz(BaseModel):
    name = TextField(max_length=1024, blank=False, null=False)
    time_limit_minutes = PositiveIntegerField(null=False)
    creator = ForeignKey(User, null=False, on_delete=CASCADE)

    def __str__(self):
        return self.name


class Question(BaseModel):
    question = TextField(max_length=256, null=False, blank=False)
    quiz = ForeignKey(Quiz, null=False, related_name='questions', on_delete=CASCADE)

    def __str__(self):
        return self.question


class PossibleAnswer(BaseModel):
    question = ForeignKey(Question, related_name='possible_answers', null=False, on_delete=CASCADE)
    answer = TextField(max_length=256, null=False, blank=False)
    is_correct = BooleanField(null=False)

    def __str__(self):
        return self.answer


class UserQuiz(BaseModel):
    email = EmailField(null=False, blank=False)
    quiz = ForeignKey(Quiz, null=False, on_delete=CASCADE)
    valid_until = DateTimeField(null=False)
    started_at = DateTimeField(null=True)
    finished_at = DateTimeField(null=True)
    results_sent = BooleanField(default=False)


class UserAnswer(BaseModel):
    user_quiz = ForeignKey(UserQuiz, related_name='user_answers', null=False, on_delete=CASCADE)
    question = ForeignKey(Question, null=False, on_delete=CASCADE)
    answer = ForeignKey(PossibleAnswer, null=True, on_delete=CASCADE)
    is_checked = BooleanField(null=True)
