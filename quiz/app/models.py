import uuid

from app.helpers import EnumType
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    PROTECT,
    BooleanField,
    DateTimeField,
    DurationField,
    EmailField,
    ForeignKey,
    Model,
    TextField,
    UUIDField,
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
    class UserType(EnumType):
        PARTICIPANT = 'PARTICIPANT'
        CREATOR = 'CREATOR'

    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user_type = TextField(choices=UserType.choices(), default=UserType.CREATOR)

    def __str__(self):
        return self.email


class Quiz(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = TextField(max_length=1024, blank=False, null=False)
    time_limit = DurationField(null=False, blank=False, help_text='ex. 1:00:00 meaning one hour')
    creator = ForeignKey(User, null=False, on_delete=CASCADE)

    def __str__(self):
        return self.name


class Question(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    question = TextField(max_length=256, null=False, blank=False)
    quiz = ForeignKey(Quiz, null=False, related_name='questions', on_delete=CASCADE)

    def __str__(self):
        return self.question


class PossibleAnswer(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    question = ForeignKey(Question, related_name='possible_answers', null=False, on_delete=CASCADE)
    answer = TextField(max_length=256, null=False, blank=False)
    is_correct = BooleanField(null=False)

    def __str__(self):
        return self.answer


class UserQuiz(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    email = EmailField(null=False, blank=False)
    user = ForeignKey(User, null=False, blank=False, on_delete=PROTECT)
    quiz = ForeignKey(Quiz, null=False, on_delete=CASCADE, related_name='userquiz')
    started_at = DateTimeField(null=True, blank=True)  # invitation accepted at
    finished_at = DateTimeField(null=True, blank=True)  # results submitted at
    results_sent = BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Invitations (User quizes)'

    def __str__(self):
        return f'{self.quiz}'


class UserAnswer(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user_quiz = ForeignKey(UserQuiz, related_name='user_answers', null=False, on_delete=CASCADE)
    question = ForeignKey(Question, null=False, on_delete=CASCADE)
    answer = ForeignKey(PossibleAnswer, null=True, on_delete=CASCADE)
    is_checked = BooleanField(null=True)
