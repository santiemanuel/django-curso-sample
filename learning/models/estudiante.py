from django.db import models
from .user import CustomUser

class Estudiante(models.Model):

    # Página 1: Información Básica
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    dob = models.DateField(verbose_name="Fecha de Nacimiento")

    # Página 2: Información Educativa y de Intereses
    NIVEL_EDUCATIVO_CHOICES = [
        ('SEC', 'Secundaria'),
        ('PRE', 'Pregrado'),
        ('POS', 'Posgrado'),
        ('OTR', 'Otro')
    ]
    nivel_educativo = models.CharField(max_length=3, choices=NIVEL_EDUCATIVO_CHOICES, default='SEC', verbose_name="Nivel Educativo", null=True, blank=True)
    interest = models.TextField(verbose_name="Intereses", null=True, blank=True)
    habilidades = models.TextField(verbose_name="Habilidades", null=True, blank=True)

    # Página 3: Información Adicional
    bio = models.TextField(verbose_name="Biografía", null=True, blank=True)
    github = models.URLField(verbose_name="GitHub", max_length=200, null=True, blank=True)
    facebook = models.URLField(verbose_name="Facebook", max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.email})"