from ..models import Curso
from django.shortcuts import render, redirect, get_object_or_404
from ..forms.curso_form import CursoForm
from django.http import HttpResponse
from ..models import Curso, Estudiante, Inscripcion

def list_cursos(request):
    """
    Listado de cursos no eliminados
    """
    cursos = Curso.objects.filter(is_deleted=False)

    busqueda = request.GET.get('search', '')

    if busqueda:
        cursos = Curso.objects.filter(descripcion__icontains=busqueda)

    context = {
        'cursos': cursos, 
        'titulo': 'Listado de Cursos',
        'busqueda': busqueda,
    }
    return render(request, "curso/cursos_list.html", context)

def detail_curso(request, curso_id):
    """
    Detalle de un curso
    """
    try:
        curso = Curso.objects.get(id=curso_id)
    except Curso.DoesNotExist:
        curso = None

    return render(request, 'curso/curso_detail.html', {'curso': curso})

def detail_curso_slug(request, slug):
    try:
        curso = Curso.objects.get(slug=slug)
    except Curso.DoesNotExist:
        curso = None

    return render(request, 'curso/curso_detail.html', {'curso': curso})

def create_curso(request):
    """
    Creación de un curso
    """
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
    """
    Actualización de un curso
    """
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
    """
    Eliminación de un curso
    """
    curso = get_object_or_404(Curso, id=curso_id)
    curso.delete()
    return redirect("list_cursos")

def hide_curso(request, curso_id):
    """
    Ocultar un curso
    """
    curso = get_object_or_404(Curso, id=curso_id)
    curso.is_deleted = True
    curso.save()
    return redirect("list_cursos")

def show_curso(request, curso_id):
    """
    Restaurar un curso
    """
    curso = get_object_or_404(Curso, id=curso_id)
    curso.is_deleted = False
    curso.save()
    return redirect("list_cursos_eliminados")

def list_cursos_eliminados(request):
    """
    Listado de cursos eliminados
    """
    cursos = Curso.objects.filter(is_deleted=True)
    context = {'cursos': cursos, 'titulo': 'Listado de Cursos Eliminados'}
    return render(request, "curso/cursos_list_restore.html", context)


def estudiante_cursos(request, estudiante_id):
    """
    Vista para mostrar los cursos en los que está inscrito un estudiante en particular, incluyendo la fecha de inscripción
    """
    try:
        estudiante = Estudiante.objects.get(pk=estudiante_id)
        inscripciones = Inscripcion.objects.filter(
            estudiante=estudiante
        ).select_related("curso")
        titulo = f"Cursos de {estudiante.nombre}"

        context = {
            'estudiante': estudiante,
            'inscripciones': inscripciones,
            'titulo': titulo
        }
        return render(request, 'estudiante/estudiantes_cursos.html', context)
    except Estudiante.DoesNotExist:
        return HttpResponse("Estudiante no encontrado", status=404)

def curso_estudiantes(request, curso_id):
    """
    Vista para mostrar los estudiantes inscritos en un curso específico
    """
    try:
        curso = Curso.objects.get(pk=curso_id)
        inscripciones = Inscripcion.objects.filter(curso=curso).select_related(
            "estudiante"
        )
        titulo = f"Estudiantes inscritos en {curso.nombre}"

        context = {
            'curso': curso,
            'inscripciones': inscripciones,
            'titulo': titulo
        }
        return render(request, 'curso/cursos_estudiantes.html', context)
    except Curso.DoesNotExist:
        return HttpResponse("Curso no encontrado", status=404)   

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

    start_month = mes_spanish[start_date.strftime("%B")]
    end_month = mes_spanish[end_date.strftime("%B")]

    context = {
        'cursos_por_mes': cursos_por_mes,
        'start_month': start_month,
        'end_month': end_month
    }

    return render(request, 'curso/cursos_fecha.html', context)