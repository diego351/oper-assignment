from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Quiz, UserQuiz

User = get_user_model()


class QuizListViewTest(TestCase):
    def test_list_quizzes(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword', user_type=User.UserType.CREATOR)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        Quiz.objects.create(name='Quiz 1', time_limit=timedelta(minutes=30), creator=user)
        Quiz.objects.create(name='Quiz 2', time_limit=timedelta(minutes=60), creator=user)

        response = client.get(reverse('quiz-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_quiz_unauthenticated(self):
        data = {'name': 'New Quiz', 'time_limit': 2400, 'questions': []}

        response = self.client.post(reverse('quiz-list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Quiz.objects.count(), 0)

    def test_invite_to_quiz(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword', user_type=User.UserType.CREATOR)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        quiz = Quiz.objects.create(name='Quiz', time_limit=timedelta(minutes=60), creator=user)
        email = 'participant@example.com'
        data = {'email': email}

        response = client.post(reverse('quiz-invite', kwargs={'quiz_id': quiz.id}), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email=email).count(), 1)

    def test_invite_to_quiz_unauthorized(self):
        email = 'participant@example.com'
        data = {'email': email}

        response = self.client.post(
            reverse('quiz-invite', kwargs={'quiz_id': '4ec404ba-593c-4a30-bb85-aba6174636eb'}), data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.filter(email=email).count(), 0)

    def test_invite_to_quiz_invalid_email(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword', user_type=User.UserType.CREATOR)
        token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        data = {'email': 'invalid-email'}

        response = client.post(
            reverse('quiz-invite', kwargs={'quiz_id': '4ec404ba-593c-4a30-bb85-aba6174636eb'}), data, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserQuiz.objects.count(), 0)
