from django.shortcuts import render
from . serializers import QuizSerializer, QuizListSerializer, QuizDetailSerializer
from .models import Quiz, Question, Option
from rest_framework import generics, viewsets

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return QuizListSerializer
        elif self.action == 'retrieve':
            return QuizDetailSerializer
        return super().get_serializer_class()        