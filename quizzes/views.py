from django.shortcuts import get_object_or_404
from . serializers import QuizSerializer, QuizListSerializer, QuizDetailSerializer, QuestionSerializer
from .models import Quiz, Question, Option
from rest_framework import viewsets

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return QuizListSerializer
        elif self.action == 'retrieve':
            return QuizDetailSerializer
        return super().get_serializer_class()

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(quiz_id=self.kwargs['quiz_pk'])

    def perform_create(self, serializer):
        quiz = get_object_or_404(Quiz, pk=self.kwargs.get('quiz_pk'))
        serializer.save(quiz=quiz)