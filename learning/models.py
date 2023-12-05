from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class CustomUser(AbstractUser):
    ESTUDIANTE = 'estudiante'
    INSTRUCTOR = 'instructor'

    ROLE_CHOICES = [
        (ESTUDIANTE, 'Estudiante'),
        (INSTRUCTOR, 'Instructor'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ESTUDIANTE)


class Instructor(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return f"{self.nombre}"


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


class Curso(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    precio = models.IntegerField()  # $250 $250.00, $262.97 => 262.97
    fecha_publicacion = models.DateField()
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    inscripciones = models.ManyToManyField(Estudiante, through="Inscripcion")
    is_deleted = models.BooleanField(default=False)

    slug = models.SlugField(max_length=120, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre}"


class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} inscrito en {self.curso}"
