from django.shortcuts import render, redirect

from django.http import HttpResponse, Http404
from .models import Curso, Estudiante, Inscripcion
from django.shortcuts import get_object_or_404
from .forms.estudiante_form import EstudianteForm, BusquedaEstudianteForm
from .forms.curso_form import CursoForm
from .forms.inscripcion_form import InscripcionForm

from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from .forms.login_form import CustomLoginForm
# Autenticación

class CustomLoginView(LoginView):
    template_name = "estudiante/estudiante_login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)

    return redirect('list_estudiantes')

# Cursos

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

# Estudiantes

def list_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    titulo = "Listado de Estudiantes"
    context = {'estudiantes': estudiantes, 'titulo': titulo}
    return render(request, "estudiante/estudiantes_list.html", context)

def detail_estudiante(request, estudiante_id):
    try:
        estudiante = Estudiante.objects.get(pk=estudiante_id)
        context = {'estudiante': estudiante}
        return render(request, 'estudiante/estudiante_detail.html', context)
    except Estudiante.DoesNotExist:
        return HttpResponse("Estudiante no encontrado", status=404)

def create_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            User = get_user_model()

            email = form.cleaned_data["email"]

            user = User.objects.create_user(username=email, email=email)
        
            nombre = form.cleaned_data['nombre']
            nombre_split = nombre.split(' ')
            user.first_name = nombre_split[0]
            user.last_name = nombre_split[-1]
            user.set_password('default')
            user.save()

            estudiante = form.save(commit=False)
            estudiante.usuario = user
            estudiante.save()
            return redirect("list_estudiantes")
    else:
        form = EstudianteForm()

    context = {
        'titulo': "Nuevo Estudiante",
        'form': form,
        'submit': 'Crear Estudiante'
    }
    return render(request, "estudiante/estudiante_form.html", context)

def update_estudiante(request, estudiante_id):
    """
    Actualización de un estudiante
    """
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect("list_estudiantes")
    else:
        form = EstudianteForm(instance=estudiante)
    context = {
        'titulo': "Actualización de Estudiante",
        'form': form,
        'submit': 'Actualizar Estudiante'
    }
    return render(request, "estudiante/estudiante_form.html", context)

# Inscripciones

def list_inscripciones(request):
    """
    Vista para listar todas las inscripciones
    """
    inscripciones = Inscripcion.objects.all().select_related("curso", "estudiante")
    titulo = "Listado de Inscripciones"
    context = {'inscripciones': inscripciones, 'titulo': titulo}
    return render(request, "inscripcion/inscripciones_list.html", context)

def inscripcion(request):
    """
    Vista para inscribir un estudiante a un curso
    """
    inscripcion_form = InscripcionForm()

    if request.method == 'POST':
        inscripcion_form = InscripcionForm(request.POST)
        if inscripcion_form.is_valid():
            inscripcion_form.save()
            return redirect('list_inscripciones')
    
    context = {
        'form': inscripcion_form,
    }
    return render(request, 'inscripcion/inscripcion_form.html', context)

def inscripcion_por_nombre(request):
    """
    Vista para inscribir un estudiante a un curso por su nombre
    """
    estudiantes = None
    inscripcion_form = InscripcionForm()
    inscripcion_form.fields['estudiante'].queryset = Estudiante.objects.none()

    if request.method == 'GET' and 'apellido' in request.GET:
        busqueda_form = BusquedaEstudianteForm(request.GET)
        if busqueda_form.is_valid():
            apellido = busqueda_form.cleaned_data['apellido']
            if apellido:
                estudiantes = Estudiante.objects.filter(nombre__icontains=apellido)
                inscripcion_form.fields['estudiante'].queryset = estudiantes
    else:
        busqueda_form = BusquedaEstudianteForm()
    
    if request.method == 'POST':
        inscripcion_form = InscripcionForm(request.POST)
        if inscripcion_form.is_valid():
            inscripcion_form.save()
            return redirect('list_inscripciones')
    
    context = {
        'busqueda_form' : busqueda_form,
        'inscripcion_form': inscripcion_form,
        'estudiantes': estudiantes,
    }
    return render(request, 'estudiante/inscripcion_form.html', context)

# Informes inscripciones/estudiantes

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