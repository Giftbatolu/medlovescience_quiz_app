from django.shortcuts import get_object_or_404
from . serializers import QuizSerializer, QuizListSerializer, QuizDetailSerializer, QuizQuestionSerializer
from .models import Quiz, Question, Option
from rest_framework import viewsets

class QuizViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing quizzes.
    Provides CRUD operations for Quiz model.
    
    get_serializer_class:
        Dynamically selects the serializer based on the action:
        - list: Uses QuizListSerializer to list all quizzes.
        - retrieve: Uses QuizDetailSerializer to provide detailed information about a specific quiz.
        - default: Uses QuizSerializer for other actions (create, update, delete).
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return QuizListSerializer
        elif self.action == 'retrieve':
            return QuizDetailSerializer
        return super().get_serializer_class()

class QuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing questions within a specific quiz.
    Provides CRUD operations for Question model filtered by quiz.

    get_queryset:
        Filters questions based on the quiz_pk provided in the URL.

    perform_create:
        Associates a new question with the specified quiz during creation.
    """
    serializer_class = QuizQuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(quiz_id=self.kwargs['quiz_pk'])

    def perform_create(self, serializer):
        quiz = get_object_or_404(Quiz, pk=self.kwargs.get('quiz_pk'))
        serializer.save(quiz=quiz)