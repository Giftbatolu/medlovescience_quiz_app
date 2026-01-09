from rest_framework import serializers
from . models import Quiz, Question, Option
from django.db import transaction

class OptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Option model

    Field:
        - id: Primary key of the option
        - option_text: Options for a quiz
        is_correct: To check for the correct answer
    """
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Question model

    This include a nested serializer for option using OptionSerializer.
    Each question can have multiple option.

    Fields:
        - id: Primary key for th question
        - question_type: The question type of the question whether OBJ or MCQ.
        - question_text: The actual question to answer.
        - explanation: Explanation for the correct answer.
        - options: Nested option for Option, which is required.
    """
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
    """
    Serializer for the Quiz model.

    This serializer includes nested serialization for questions using QuestionSerializer.
    Each question can have multiple options, which are handled during creation.

    Fields:
        - id: Primary key of the quiz.
        - quiz_name: Name or title of the quiz.
        - questions: Nested list of questions associated with the quiz, optional.

    create(validated_data):
        Overrides the default create method to handle nested question and option data.
        - Extracts questions data from the validated data.
        - Uses a database transaction to ensure atomic creation of quiz, questions, and options.
        - Iterates over each question and its options to create related objects.
        - Returns the created Quiz instance.

    update(instance, validate):
        Update the quiz name of the instance of created quiz
        
    validate_quiz_name(self, value):
        validate to ensure unique quiz name i.e n two with the same quiz title
    """

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
    
    def validate_quiz_name(self, value):
        if Quiz.objects.filter(quiz_name__iexact=value).exists():
            raise serializers.ValidationError("Quiz title already exists.")
        return value

class QuizListSerializer(serializers.ModelSerializer):
    """
    Serializer to list all available quiz

    Fields:
        - id: Primary key of the quiz.
        - quiz_name: Name of the quiz
    """
    class Meta:
        model = Quiz
        fields = [
            'id',
            'quiz_name',
        ]

class QuizDetailSerializer(serializers.ModelSerializer):
    """
    Serializer to give detail about a quiz
    It include computation field for question type and total question for the the quiz

    Fields:
        - id: PRimary key
        - quiz_name: Name of the quiz
        - question_type: Question type
        - tota_question: Total question for a quiz

    qet_question_type
        A function that get the question type of the first question and return it

    qet_total_question
        A funtion that count and return all question in a quiz
    """
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
        """
        first_question = obj.questions.first()
        return first_question.question_type if first_question else None

    def get_total_question(self, obj):
        return obj.questions.count()

class BulkQuestionListSerializer(serializers.ListSerializer):
    """
    Serializer used to add more than one question to a quiz.

    create(validated_data):
        Overides the default create method to handle bulk creation of questions and options.
        - Creates multiple Question instances along with their associated Option instances in a single operation.
        - Uses the context to get the quiz to which the questions belong.
        - Iterates over the validated data to create each question and its options.
        - Returns the list of created Question instances.
    """
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
    """
    Serializer for adding question to a quiz in bulk.

    Fields:
        - id: Primary key for the question
        - question_type: The question type of the question whether OBJ or MCQ.
        - question_text: The actual question to answer.
        - explanation: Explanation for the correct answer.
        - options: Nested option for Option, which is required.

    Meta:
        - list_serializer_class: Specifies the use of BulkQuestionListSerializer for bulk operations.

    create(validated_data):
        Overrides the default create method to handle nested question and option data for a single question.
    
    update(instance, validated_data):
        Overrides the default update method to handle nested question and option data for updating a question.
        
    validate(self, data):
        Validate that no question appear twice in a quiz
    """
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
        list_serializer_class = BulkQuestionListSerializer

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        quiz = self.context.get('quiz')
        question = Question.objects.create(quiz=quiz, **validated_data)

        for option_data in options_data:
            Option.objects.create(question=question, **option_data)

        return question

    def update(self, instance, validated_data):
        option_data = validated_data.pop('options', [])

        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.explanation = validated_data.get('explanation', instance.explanation)
        instance.save()

        if option_data:
            instance.options.all().delete()
            for option in option_data:
                Option.objects.create(question=instance, **option)

        return instance
    
    def validate(self, data):
        quiz = data.get("quiz")
        question_text = data.get("question_text")

        if Question.objects.filter(quiz=quiz, question_text__iexact=question_text).exists():
            raise serializers.ValidationError("This question already exists in this quiz.")

        return data