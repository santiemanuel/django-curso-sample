from django.db import models
from .user import CustomUser

class Estudiante(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    dob = models.DateField(verbose_name="Fecha de Nacimiento")
    bio = models.TextField(verbose_name="Biografía", null=True, blank=True)
    interest = models.TextField(verbose_name="Intereses", null=True, blank=True)
    github = models.URLField(verbose_name="GitHub", max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.email})"