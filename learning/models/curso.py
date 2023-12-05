from django.db import models
from .instructor import Instructor
from .estudiante import Estudiante
from django.utils.text import slugify


class Curso(models.Model):

    # Página 1: Información General del Curso
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    precio = models.IntegerField()

    # Página 2: Detalles y Metodología del Curso
    METODOLOGIA_CHOICES = [
        ('online', 'Online'),
        ('presencial', 'Presencial'),
        ('semipresencial', 'Semipresencial'),
    ]
    metodologia = models.CharField(max_length=15, choices=METODOLOGIA_CHOICES, default='online', verbose_name="Metodología del Curso")
    objetivos = models.TextField(verbose_name="Objetivos del Curso", null=True, blank=True)
    contenido = models.TextField(verbose_name="Contenido del Curso", null=True, blank=True)

    # Página 3: Información Complementaria
    fecha_publicacion = models.DateField()
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)

    # Datos internos
    inscripciones = models.ManyToManyField(Estudiante, through="Inscripcion")
    slug = models.SlugField(max_length=120, unique=True, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre}"