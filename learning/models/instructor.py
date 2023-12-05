from django.db import models
from .user import CustomUser

class Instructor(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return f"{self.nombre}"