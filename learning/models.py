from django.db import models
from django.db.models.query import QuerySet


class FreeCoursesManager(models.Manager):
    """Manager para obtener todos los cursos gratis."""

    def get_queryset(self):
        return super().get_queryset().filter(precio=0)


class PremiumCoursesManager(models.Manager):
    """Manager para obtener todos los cursos premium."""

    def get_queryset(self):
        return super().get_queryset().filter(precio__gt=600)


class CursoByYearManager(models.Manager):
    """Manager para obtener los cursos por año."""

    def courses_in_year(self, year):
        return self.filter(fecha_publicacion__year=year)


class CursoByTopicManager(models.Manager):
    """Manager para obtener los cursos por temática."""

    def courses_for_topic(self, topic_name):
        # Este es un ejemplo simple. En la realidad, deberíamos crear un campo o modelo independiente para los temas.
        return self.filter(nombre__icontains=topic_name)


class Instructor(models.Model):
    nombre = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return f"{self.nombre}"


class Estudiante(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    dob = models.DateField(verbose_name="Fecha de Nacimiento")
    bio = models.TextField(verbose_name="Biografía", null=True, blank=True)
    interest = models.TextField(verbose_name="Intereses", null=True, blank=True)
    github = models.URLField(verbose_name="GitHub", max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.email})"


# Create your models here.
class Curso(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    precio = models.IntegerField()  # $250 $250.00, $262.97 => 262.97
    fecha_publicacion = models.DateField()
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    inscripciones = models.ManyToManyField(Estudiante, through="Inscripcion")
    is_deleted = models.BooleanField(default=False)

    # free_courses = FreeCoursesManager()
    # premium_courses = PremiumCoursesManager()
    # by_year = CursoByYearManager()
    # by_topic = CursoByTopicManager()

    def __str__(self):
        return f"{self.nombre}"


class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} inscrito en {self.curso}"
