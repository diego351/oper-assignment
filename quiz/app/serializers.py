from dataclasses import dataclass
from typing import List

from app.email_service import EmailService
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.fields import BooleanField, EmailField, UUIDField
from rest_framework.serializers import ModelSerializer, Serializer

from .models import *


class CreatorPossibleAnswerSerialiser(ModelSerializer):
    class Meta:
        model = PossibleAnswer

        fields = ('id', 'answer', 'is_correct')


class CreatorQuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'possible_answers')

    possible_answers = CreatorPossibleAnswerSerialiser(many=True)


class CreatorQuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'time_limit', 'questions']

    questions = CreatorQuestionSerializer(many=True)

    def create(self, validated_data):
        quiz_instance = Quiz.objects.create(
            name=validated_data.get('name'),
            time_limit=validated_data.get('time_limit'),
            creator=self.context['request'].user,
        )
        for question in validated_data.get('questions'):
            question_instance = Question.objects.create(
                question=question.get('question'),
                quiz=quiz_instance,
            )
            for possible_answer in question.get('possible_answers'):
                PossibleAnswer.objects.create(
                    question=question_instance,
                    answer=possible_answer.get('answer'),
                    is_correct=possible_answer.get('is_correct'),
                )

        return quiz_instance


class ParticipantPossibleAnswerSerialiser(ModelSerializer):
    class Meta:
        model = PossibleAnswer

        fields = ('id', 'answer')


class ParticipantQuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'possible_answers')

    possible_answers = ParticipantPossibleAnswerSerialiser(many=True)


class ParticipantQuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'time_limit', 'questions']

    questions = ParticipantQuestionSerializer(many=True)


class UserQuizSerializer(ModelSerializer):
    class Meta:
        model = UserQuiz
        fields = ('quiz',)

    quiz = ParticipantQuizSerializer()


class InviteToQuizSerializer(Serializer):
    email = EmailField()

    def create(self, validated_data):
        email = validated_data.get('email')
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                'user_type': User.UserType.PARTICIPANT,
                'username': email,
            },
        )
        token, _ = Token.objects.get_or_create(user=user)

        try:
            quiz = Quiz.objects.get(id=self.context['request'].quiz_id)

        except Quiz.DoesNotExist:
            raise ValidationError('Quiz does not exist')

        instance = UserQuiz.objects.create(
            user=user,
            quiz=quiz,
            email=email,
        )

        EmailService.send_invitation(email, token, quiz.id)

        return instance


class UserAnswerSerializer(Serializer):
    answer = UUIDField()
    is_checked = BooleanField()


class UserAnswerListSerializer(Serializer):
    question = UUIDField()
    answers = UserAnswerSerializer(many=True)

    def create(self, validated_data):
        user = self.context['request'].user
        user_quiz_id = self.context['request'].user_quiz_id

        try:
            user_quiz = UserQuiz.objects.get(id=user_quiz_id, user=user)
            quiz = user_quiz.quiz
        except UserQuiz.DoesNotExist:
            raise NotFound('Quiz not found')

        try:
            question = quiz.questions.get(id=validated_data.get('question'))

        except Question.DoesNotExist:
            raise NotFound('Question not found')

        answers = []
        for answer_data in validated_data.get('answers'):
            try:
                answer = question.possible_answers.get(id=answer_data.get('answer'))

            except PossibleAnswer.DoesNotExist:
                raise NotFound('Answer not found')

            is_checked = answer_data.get('is_checked')

            answer, created = UserAnswer.objects.update_or_create(
                user_quiz=user_quiz,
                question=question,
                answer=answer,
                defaults={
                    'is_checked': is_checked,
                },
            )
            answers.append(answer)

        @dataclass
        class RetObject:
            question: Question
            answers: List

        return RetObject(question=question, answers=answers)
