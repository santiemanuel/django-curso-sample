from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, Http404
from .models import Curso, Estudiante, Inscripcion
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import datetime
from .forms.estudiante_form import EstudianteForm
from .forms.curso_form import CursoForm

# Estilo base para aplicar a todas las respuestas
base_style = """
<style>
    body { 
        font-family: Roboto, sans-serif;
        line-height: 1.6;
        margin: 20px; 
    }

    h1 { 
        color: #333;
        margin-bottom: 20px;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        background: #ffd5ae;
        margin: 5px 0;
        padding: 10px;
        width: 50%;
        border-radius: 16px;
        margin-bottom: 16px;
    }

    .curso-nombre {
        font-size: 1.2em;
        margin: 0;
    }

    .curso-title {
        font-size: 1.6em;
        font-weight: bold;
        margin: 0;
    }

    .curso-details {
        font-size: 0.8em;
        color: #777;
        margin-top: 4px;
    }

    .fecha-inscripcion {
        font-size: 0.8em;
        color: #777;
        margin-top: 4px;
    }

    p {
        color: #666;
    }

    a {
        color: #8baccc;
    }
</style>
"""


def list_cursos(request):
    cursos = Curso.objects.filter(is_deleted=False)
    context = {'cursos': cursos, 'titulo': 'Listado de Cursos'}
    return render(request, "curso/cursos_list.html", context)


def list_cursos_eliminados(request):
    cursos = Curso.objects.filter(is_deleted=True)
    context = {'cursos': cursos, 'titulo': 'Listado de Cursos Eliminados'}
    return render(request, "curso/cursos_list_restore.html", context)


# Vista para mostrar información detallada de un curso específico
def detail_curso_pre(request, curso_id):
    try:
        curso = Curso.objects.get(pk=curso_id)
        response_html = (
            base_style
            + f"""
            <h1>Detalle del Curso: {curso.nombre}</h1>
            <p><strong>Descripción:</strong> {curso.descripcion}</p>
            <p><strong>Precio:</strong> {curso.precio}$</p>
            <p><strong>Fecha de Publicación:</strong> {curso.fecha_publicacion}</p>
        """
        )
        return HttpResponse(response_html)
    except Curso.DoesNotExist:
        return HttpResponse(base_style + "Curso no encontrado", status=404)
    
def detail_curso(request, curso_id):
    try:
        curso = Curso.objects.get(id=curso_id)
    except Curso.DoesNotExist:
        curso = None

    return render(request, 'curso/curso_detail.html', {'curso': curso})

def create_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_cursos")
    else:
        form = CursoForm()

    context = {
        'titulo': "Nuevo Curso",
        'form': form,
        'submit': 'Crear Curso'
    }
    return render(request, "curso/curso_form.html", context)

def update_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect("list_cursos")
    else:
        form = CursoForm(instance=curso)
    context = {
        'titulo': "Actualización de Curso",
        'form': form,
        'submit': 'Actualizar Curso'
    }
    return render(request, "curso/curso_form.html", context)

def delete_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    curso.delete()
    return redirect("list_cursos")

def hide_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    curso.is_deleted = True
    curso.save()
    return redirect("list_cursos")

def restore_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    curso.is_deleted = False
    curso.save()
    return redirect("list_cursos_eliminados")

def create_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_estudiantes")
    else:
        form = EstudianteForm()

    context = {
        'titulo': "Nuevo Estudiante",
        'form': form,
        'submit': 'Crear Estudiante'
    }
    return render(request, "estudiante/estudiante_form.html", context)



# Vista para listar todos los estudiantes
def list_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    response_html = base_style + "<h1>Listado de Estudiantes</h1><ul>"
    response_html += "".join(
        [
            f'<li>{estudiante.nombre} - <a href="{estudiante.email}"> {estudiante.email}</a></li>'
            for estudiante in estudiantes
        ]
    )
    response_html += "</ul>"
    return HttpResponse(response_html)


# Vista para mostrar los cursos en los que está inscrito un estudiante en particular, incluyendo la fecha de inscripción
def estudiante_cursos(request, estudiante_id):
    try:
        estudiante = Estudiante.objects.get(pk=estudiante_id)
        inscripciones = Inscripcion.objects.filter(
            estudiante=estudiante
        ).select_related("curso")
        response_html = base_style + f"<h1>Cursos de {estudiante.nombre}</h1><ul>"

        for inscripcion in inscripciones:
            fecha_inscripcion = inscripcion.fecha_inscripcion.strftime(
                "%d/%m/%Y"
            )  # Formatea la fecha
            response_html += f"""
                <li>
                    <div class="curso-nombre">{inscripcion.curso.nombre}</div>
                    <div class="fecha-inscripcion">Inscrito el {fecha_inscripcion}</div>
                </li>
            """

        response_html += "</ul>"
        return HttpResponse(response_html)
    except Estudiante.DoesNotExist:
        return HttpResponse(base_style + "Estudiante no encontrado", status=404)


# Vista para listar todas las inscripciones
def list_inscripciones(request):
    inscripciones = Inscripcion.objects.all().select_related("curso", "estudiante")
    response_html = base_style + "<h1>Listado de Inscripciones</h1><ul>"
    response_html += "".join(
        [
            f"<li>{inscripcion.estudiante.nombre} inscrito en {inscripcion.curso.nombre}</li>"
            for inscripcion in inscripciones
        ]
    )
    response_html += "</ul>"
    return HttpResponse(response_html)


# Vista para mostrar los estudiantes inscritos en un curso específico
def curso_estudiantes(request, curso_id):
    try:
        curso = Curso.objects.get(pk=curso_id)
        inscripciones = Inscripcion.objects.filter(curso=curso).select_related(
            "estudiante"
        )
        response_html = base_style + f"<h1>Estudiantes inscritos en {curso.nombre}</h1>"

        if inscripciones.exists():  # Verifica si hay inscripciones
            response_html += "<ul>"
            response_html += "".join(
                [
                    f"<li>{inscripcion.estudiante.nombre}</li>"
                    for inscripcion in inscripciones
                ]
            )
            response_html += "</ul>"
        else:
            response_html += "<p>Todavía no hay estudiantes inscritos.</p>"

        return HttpResponse(response_html)
    except Curso.DoesNotExist:
        return HttpResponse(base_style + "Curso no encontrado", status=404)


def cursos_por_fecha(request, date_range):
    start_date, end_date = date_range
    cursos = Curso.objects.filter(
        fecha_publicacion__range=(start_date, end_date)
    ).order_by("fecha_publicacion")

    # Diccionario para traducir los nombres de los meses a español.
    mes_spanish = {
        "January": "Enero",
        "February": "Febrero",
        "March": "Marzo",
        "April": "Abril",
        "May": "Mayo",
        "June": "Junio",
        "July": "Julio",
        "August": "Agosto",
        "September": "Septiembre",
        "October": "Octubre",
        "November": "Noviembre",
        "December": "Diciembre",
    }

    cursos_por_mes = {}

    for curso in cursos:
        mes = curso.fecha_publicacion.strftime("%B")
        mes_es = mes_spanish[mes]
        if mes_es not in cursos_por_mes:
            cursos_por_mes[mes_es] = []
        cursos_por_mes[mes_es].append(curso)

    # Inicio de respuesta HTML.
    start_month = mes_spanish[start_date.strftime("%B")]
    end_month = mes_spanish[end_date.strftime("%B")]
    response_html = (
        f"<h1>Cursos a dictarse en el rango: {start_month} a {end_month}</h1>"
    )

    for mes_esp in mes_spanish.values():
        if mes_esp in cursos_por_mes:
            response_html += f"<h2>{mes_esp}</h2><ul>"
            for curso in cursos_por_mes[mes_esp]:
                fecha_publicacion = curso.fecha_publicacion.strftime(
                    "%d/%m/%Y"
                )  # Formatea la fecha
                response_html += f"""
                    <li class='item-curso'>
                        <div class="curso-nombre">{curso.nombre}</div>
                        <div class="fecha-inscripcion">Fecha de publicación: {fecha_publicacion}</div>
                    </li>
                """
            response_html += "</ul>"

    response_html = base_style + response_html
    return HttpResponse(response_html)
