from rest_framework import serializers
from . models import Quiz, Question, Option

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
            # 'id', 
            'question_type', 
            'question_text', 
            'explanation',
            'options'
        ]

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)

        for option_data in options_data:
            Option.objects.create(question=question, **option_data)

        return question

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
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            options_data = question_data.pop('options')
            question = Question.objects.create(quiz=quiz, **question_data)

            for option_data in options_data:
                Option.objects.create(question=question, **option_data)

        return quiz

    def update(self, instance, validated_data):
        # Update quiz fields
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

class QuestionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [

            'question_type',
        ]

class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionDetailSerializer(many=True)
    
    class Meta:
        model = Quiz
        fields = [
            'id',
            'quiz_name',
            'questions',
        ]