from django.db import models
from django.cnf import settings
from quizzes.models import Quiz, Question

class Attempt(models.Model):

    STATUS_CHOICES = [
        ('in_progress', 'In progress'),
        ('submitted', 'Submitted'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES, 
        default='in_progress'
    )
    
    score = models.IntegerField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(
        Attempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    answer = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(null=True)
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('attempt', 'question')