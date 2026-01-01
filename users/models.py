from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('contributor', 'Contributor'),
    )

    role = models.CharField(max_length=20, choices=ROLES, default='student')
    email = models.EmailField(unique=True)