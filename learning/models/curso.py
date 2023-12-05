from django.db import models
from .instructor import Instructor
from .estudiante import Estudiante
from django.utils.text import slugify


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