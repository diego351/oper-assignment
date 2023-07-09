from app.views import (
    InviteToQuizView,
    ParticipantAcceptInvitation,
    QuizListView,
    RetriveUserQuizView,
    SpectacularElementsView,
    UploadUserAnswerView,
)
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema', SpectacularAPIView.as_view(), name="schema"),
    path('docs', SpectacularElementsView.as_view()),
    path('api/quizes', QuizListView.as_view(), name='quiz-list'),
    path('api/quizes/<uuid:quiz_id>/invite', InviteToQuizView.as_view(), name='quiz-invite'),
    path('api/quizes/<uuid:pk>/accept', ParticipantAcceptInvitation.as_view(), name='quiz-accept-invitation'),
    path('api/user_quizes/<uuid:pk>', RetriveUserQuizView.as_view(), name='user-quiz-detail'),
    path('api/user_quizes/<uuid:pk>/answers', UploadUserAnswerView.as_view(), name='user-answer-upload'),
]
