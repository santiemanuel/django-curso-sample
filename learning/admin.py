from django.contrib import admin
from .models import Curso
from .models import Estudiante
from .models import Inscripcion
from .models import Instructor

# Register your models here.


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    fields = ["nombre", "descripcion", ("fecha_publicacion", "precio"), "instructor"]
    list_display = ("nombre", "descripcion", "precio", "fecha_publicacion")
    search_fields = ("nombre", "descripcion")
    list_filter = ("precio", "fecha_publicacion")
    ordering = ("nombre", "-precio")


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    fields = ["nombre", "email", 'avatar', 'dob', 'bio', 'interest', 'github']
    list_display = ("nombre", "email", 'avatar')
    search_fields = ("nombre", "email")
    ordering = ("nombre", "email")


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    fields = ["estudiante", "curso"]
    readonly_fields = ("fecha_inscripcion",)
    list_display = ("curso", "estudiante", "fecha_inscripcion")
    search_fields = ("curso__nombre", "estudiante__nombre")
    ordering = ("curso", "estudiante")


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    fields = ["nombre", "bio"]
    list_display = ("nombre", "bio")
    search_fields = ("nombre", "bio")
    ordering = ("nombre", "bio")
