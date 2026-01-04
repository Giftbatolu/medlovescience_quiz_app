from django.urls import path
from . import views

urlpatterns = [
    path('', views.StartAttemptView.as_view(), name='start-attempt'),
    path('<int:attempt_id>/answer/<int:question_id>/', views.AttemptAnswerView.as_view(), name='attempt-answer'),
]