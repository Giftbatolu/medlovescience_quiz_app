from rest_framework import serializers
from . models import Quiz, Question, Option
from django.db import transaction

class OptionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    class Meta:
        model = Question
        fields = [
            'id', 
            'question_type', 
            'question_text', 
            'explanation',
            'options'
        ]

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)
    class Meta:
        model = Quiz
        fields = [
            'id',
            'quiz_name',
            'questions'

            ]

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')

        with transaction.atomic():
            quiz = Quiz.objects.create(**validated_data)

            for question_data in questions_data:
                options_data = question_data.pop('options')
                question = Question.objects.create(quiz=quiz, **question_data)

                for option_data in options_data:
                    Option.objects.create(question=question, **option_data)

        return quiz

    def update(self, instance, validated_data):
        instance.quiz_name = validated_data.get('quiz_name', instance.quiz_name)
        instance.save()
        return instance

class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            'id',
            'quiz_name',
        ]

class QuizDetailSerializer(serializers.ModelSerializer):
    question_type = serializers.SerializerMethodField()
    total_question = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            'id',
            'quiz_name',
            'question_type',
            'total_question',
        ]

    def get_question_type(self, obj):
        """
        Returns the question_type.
        If your quiz has multiple types, you can decide how to handle it.
        """
        first_question = obj.questions.first()
        return first_question.question_type if first_question else None

    def get_total_question(self, obj):
        return obj.questions.count()

class BulkQuestionListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        quiz = self.context['quiz']
        questions = []

        for question_data in validated_data:
            options_data = question_data.pop('options', [])
            question = Question.objects.create(quiz=quiz, **question_data)

            options = [
                Option(question=question, **option_data)
                for option_data in options_data
            ]
            Option.objects.bulk_create(options)

            questions.append(question)

        return questions

class QuizQuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)
    
    class Meta:
        model = Question
        fields = [
            'id', 
            'question_type', 
            'question_text', 
            'explanation',
            'options'
        ]
        list_serializer_class = BulkQuestionListSerializer