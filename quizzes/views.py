from django.shortcuts import render
from . serializers import QuestionSerializer, OptionSerializer, QuizSerializer, QuizListSerializer
from .models import Quiz, Question, Option
from rest_framework import generics, viewsets

class QuizView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = []

class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    permission_classes = []