from django.shortcuts import get_object_or_404
from .models import Attempt, AttemptAnswer
from .serializers import StartAttemptSerializer, StudentQuestionSerializer, AttemptAnswerSerializer
from quizzes.models import Question, Option
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view

class StartAttemptView(APIView):
    def post(self, request):
        serializer = StartAttemptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quiz = serializer.validated_data['quiz_id']

        attempt = Attempt.objects.create(
            user=request.user,
            quiz=quiz,
            status='in_progress'
        )
        first_question = quiz.questions.first()

        question_serializer = StudentQuestionSerializer(
            first_question,
            context={'attempt': attempt}
        )

        return Response(
            question_serializer.data,
            status=status.HTTP_201_CREATED
        )

class AttemptAnswerView(APIView):
    def put(self, request, attempt_id, question_id):
        attempt = get_object_or_404(Attempt, id=attempt_id, user=request.user)

        if attempt.status == 'submitted':
            return Response(
                {"detail": "Cannot update answers. Attempt has been submitted."},
                status=status.HTTP_403_FORBIDDEN
            )
           
        question = get_object_or_404(
            Question,
            id=question_id,
            quiz=attempt.quiz
            )

        serializer = AttemptAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answer = get_object_or_404(
            Option,
            id=serializer.validated_data['answer_id'],
            question=question
        )

        attempt_answer, created = AttemptAnswer.objects.get_or_create(
            attempt=attempt,
            question=question,
            defaults={'answer': answer}
        )

        if not created:
            attempt_answer.answer = answer
            attempt_answer.save()

        answered_questions = attempt.answers.values_list('question_id', flat=True)
        next_question = attempt.quiz.questions.exclude(id__in=answered_questions).first()

        if not next_question:
            return Response({"detail": "Quiz completed"}, status=status.HTTP_200_OK)

        next_question_serializer = StudentQuestionSerializer(next_question, context={'attempt': attempt})
        return Response(next_question_serializer.data)