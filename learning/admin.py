from django.contrib import admin
from .models import Curso

# Register your models here.


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    fields = ["nombre", "descripcion", ("fecha_publicacion", "precio")]
    list_display = ("nombre", "descripcion", "precio", "fecha_publicacion")
    search_fields = ("nombre", "descripcion")
    list_filter = ("precio", "fecha_publicacion")
    ordering = ("nombre", "-precio")
