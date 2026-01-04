from quizzes.models import Question, Quiz, Option
from . models import Attempt, AttemptAnswer
from rest_framework import serializers

class StartAttemptSerializer(serializers.Serializer):
    quiz_id = serializers.PrimaryKeyRelatedField(
        queryset=Quiz.objects.all()
    )


class AttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = ['id']

class StudentOptionSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Option
        fields = ['id', 'option_text']

class StudentQuestionSerializer(serializers.ModelSerializer):
    options = StudentOptionSerializer(many=True)
    attempt_id = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id',
            'question_type',
            'question_text',
            'options',
            'attempt_id'
        ]
    
    def get_attempt_id(self, obj):
        attempt = self.context.get('attempt')
        if attempt:
            return attempt.id
        return None

class AttemptAnswerSerializer(serializers.Serializer):
    answer_id = serializers.UUIDField()

    # def validate(self, data):
    #     # Check question exists
    #     question = get_object_or_404(Question, id=data['question_id'])
    #     data['question'] = question

    #     # Check option belongs to the question
    #     option = get_object_or_404(Option, id=data['selected_option_id'])
    #     if option.question_id != question.id:
    #         raise serializers.ValidationError("Option does not belong to the question")
    #     data['option'] = option

    #     return data
