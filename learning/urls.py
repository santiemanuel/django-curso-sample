from django.urls import path, register_converter
from django.conf import settings
from django.conf.urls.static import static

from . import converters

from .views import curso_views
from .views import estudiante_views
from .views import inscripcion_views
from .views import login_views

register_converter(converters.DateRangeConverter, "daterange")


urlpatterns = [
    # Autenticación

    path("login/", login_views.CustomLoginView.as_view(), name='login'),
    path("logout/", login_views.logout_view, name="logout"),

    # Cursos
    path("cursos/", 
         curso_views.list_cursos,
         name="list_cursos"),
    path("cursos/<slug:slug>/",
         curso_views.detail_curso_slug,
         name="detail_curso_slug"),
    path("cursos/<int:curso_id>/",
         curso_views.detail_curso,
         name="detail_curso"),
    path("cursos/crear",
         curso_views.create_curso,
         name="create_curso"),
    path("cursos/actualizar/<int:curso_id>/",
         curso_views.update_curso,
         name="update_curso"),
    path("cursos/eliminar/<int:curso_id>/",
         curso_views.delete_curso,
         name="delete_curso"),
    path("cursos/ocultar/<int:curso_id>/",
         curso_views.hide_curso,
         name="hide_curso"),
    path("cursos/mostrar/<int:curso_id>/",
         curso_views.show_curso,
         name="show_curso"),
    path("cursos_eliminados/",
         curso_views.list_cursos_eliminados,
         name="list_cursos_eliminados"),
    # Estudiantes 
     path("estudiantes/",
         estudiante_views.list_estudiantes,
         name="list_estudiantes"),
     path("estudiantes/<int:estudiante_id>/",
         estudiante_views.detail_estudiante,
         name="detail_estudiante"),    
     path("estudiantes/crear/",
         estudiante_views.create_estudiante,
         name="create_estudiante"),
     path("estudiantes/actualizar/<int:estudiante_id>/",
         estudiante_views.update_estudiante,
         name="update_estudiante"),
    # Inscripciones
     path("inscripciones/",
         inscripcion_views.list_inscripciones,
         name="list_inscripciones"),
     path("inscripcion/",
         inscripcion_views.inscripcion,
         name="inscribir"),
     path("inscripcion-nombre/",
         inscripcion_views.inscripcion_por_nombre,
         name="inscribir-nombre"),
    # Informes inscripciones/estudiantes
     path(
        "estudiantes/<int:estudiante_id>/cursos/",
        curso_views.estudiante_cursos,
        name="estudiante_cursos",
    ),
     path(
        "cursos/<int:curso_id>/estudiantes/",
        curso_views.curso_estudiantes,
        name="curso_estudiantes",
    ),
     path(
        "cursos/<daterange:date_range>/",
        curso_views.cursos_por_fecha,
        name="cursos-por-fecha",
    )
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)