from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ESTUDIANTE = 'estudiante'
    INSTRUCTOR = 'instructor'

    ROLE_CHOICES = [
        (ESTUDIANTE, 'Estudiante'),
        (INSTRUCTOR, 'Instructor'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ESTUDIANTE)