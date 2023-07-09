from app.serializers import (
    CreatorQuizSerializer,
    InviteToQuizSerializer,
    ParticipantQuizSerializer,
    UserAnswerListSerializer,
    UserQuizSerializer,
)
from django.db.models import F
from django.utils import timezone
from django_filters import CharFilter
from django_filters import rest_framework as filters
from drf_spectacular.settings import spectacular_settings
from drf_spectacular.utils import OpenApiParameter, PolymorphicProxySerializer, extend_schema, extend_schema_view
from drf_spectacular.views import AUTHENTICATION_CLASSES
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *


class SpectacularElementsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = spectacular_settings.SERVE_PERMISSIONS
    authentication_classes = AUTHENTICATION_CLASSES
    url_name = 'schema'
    url = None
    template_name = 'elements.html'
    title = spectacular_settings.TITLE

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return Response(
            data={
                'title': self.title,
                'js_dist': 'https://unpkg.com/@stoplight/elements/web-components.min.js',
                'css_dist': 'https://unpkg.com/@stoplight/elements/styles.min.css',
                'schema_url': '/schema',
            },
            template_name=self.template_name,
        )


class QuizFilter(filters.FilterSet):
    name_contains = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Quiz
        fields = ("name_contains",)


@extend_schema_view(
    get=extend_schema(
        parameters=[OpenApiParameter(name='name_contains', description='Name filter', type=str)],
        responses={
            200: PolymorphicProxySerializer(
                component_name='Person',
                serializers=[CreatorQuizSerializer, ParticipantQuizSerializer],
                resource_type_field_name='type',
            )
        },
    ),
    post=extend_schema(request=CreatorQuizSerializer, responses={201: CreatorQuizSerializer}),
)
class QuizListView(CreateAPIView, ListAPIView):
    serializer_class = CreatorQuizSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    filterset_class = QuizFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.user.user_type == User.UserType.CREATOR:
            return CreatorQuizSerializer

        elif self.request.user.user_type == User.UserType.PARTICIPANT:
            return ParticipantQuizSerializer

        else:
            raise NotImplementedError

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        elif request.method == 'POST' and request.user.user_type != User.UserType.CREATOR:
            return False

    def get_queryset(self):
        qs = Quiz.objects

        if self.request.user.user_type == User.UserType.CREATOR:
            qs = qs.filter(creator=self.request.user)

        elif self.request.user.user_type == User.UserType.PARTICIPANT:
            now = timezone.now()
            qs = qs.filter(userquiz__started_at__isnull=False)
            qs = qs.filter(userquiz__finished_at__isnull=True)
            qs = qs.filter(userquiz__user=self.request.user)
            qs = qs.filter(userquiz__started_at__lte=now - F('time_limit'))

        qs = qs.prefetch_related('questions').prefetch_related('questions__possible_answers')

        return qs.all()


class InviteToQuizView(CreateAPIView):
    serializer_class = InviteToQuizSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, quiz_id, *args, **kwargs):
        request.quiz_id = quiz_id

        return super().post(request, quiz_id, *args, **kwargs)


class RetriveUserQuizView(RetrieveAPIView):
    serializer_class = UserQuizSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = UserQuiz.objects

        now = timezone.now()
        qs = qs.filter(started_at__isnull=False)
        qs = qs.filter(finished_at__isnull=True)
        qs = qs.filter(user=self.request.user)
        qs = qs.filter(started_at__lte=now - F('quiz__time_limit'))

        qs = qs.prefetch_related('quiz__questions').prefetch_related('quiz__questions__possible_answers')

        return qs.all()


class ParticipantAcceptInvitation(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            user_quiz = UserQuiz.objects.get(
                quiz_id=pk,
                started_at__isnull=True,
                finished_at__isnull=True,
                user=self.request.user,
            )
        except UserQuiz.DoesNotExist:
            raise NotFound('Either not found or already started')

        user_quiz.started_at = timezone.now()
        user_quiz.save()
        return Response({'user_quiz_id': user_quiz.id}, 200)


class UploadUserAnswerView(CreateAPIView):
    serializer_class = UserAnswerListSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        request.user_quiz_id = pk
        return super().post(request, pk)
