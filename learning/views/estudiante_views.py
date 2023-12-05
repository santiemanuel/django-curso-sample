from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..models import Estudiante
from ..forms.estudiante_form import EstudianteFormPasoUno, EstudianteFormPasoDos, EstudianteFormPasoTres

from django.contrib.auth import get_user_model
from datetime import date, datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.core.files import File
from django.core.files.storage import default_storage

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
    prev_step = request.GET.get('prev_step')
    if prev_step:
        current_step = int(prev_step)
    else:
        current_step = request.session.get('step', 1)

    next_step = None
    previous_step = current_step - 1 if current_step > 1 else None
    request.session['step'] = current_step

    if request.method == 'POST':
        if current_step == 1:
            form = EstudianteFormPasoUno(request.POST, request.FILES)
            next_step = 2
        elif current_step == 2:
            form = EstudianteFormPasoDos(request.POST)
            next_step = 3
        else:  # Paso 3
            form = EstudianteFormPasoTres(request.POST)
            next_step = None

        if form.is_valid():
            data_estudiante = form.cleaned_data
            for key, value in data_estudiante.items():
                if isinstance(value, date):
                    value = value.strftime('%Y-%m-%d')
                request.session[key] = value

            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
                filename = fs.save(avatar.name, avatar)
                request.session['avatar'] = filename

            if next_step:
                request.session['step'] = next_step
                return redirect("create_estudiante")
            else:
                # Guardo última info cargada para poder regresar
                User = get_user_model()

                email = request.session.get("email")
                nombre = request.session.get("nombre")

                user = User.objects.create_user(username=email, email=email)
                nombre_split = nombre.split(' ')
                user.first_name = nombre_split[0]
                if len(nombre_split) > 1:
                    user.last_name = nombre_split[-1]
                user.set_password('default')
                user.save()

                estudiante = Estudiante(usuario=user)
                estudiante.nombre = nombre
                estudiante.email = email

                estudiante.dob = request.session.get("dob")
                estudiante.nivel_educativo = request.session.get("nivel_educativo")
                estudiante.interest = request.session.get("interest")
                estudiante.habilidades = request.session.get("habilidades")
                estudiante.bio = form.cleaned_data.get("bio")
                estudiante.github = form.cleaned_data.get("github")
                estudiante.facebook = form.cleaned_data.get("facebook")
                estudiante.save()

                imagen_path = request.session.get('avatar')
                if imagen_path:
                    imagen_full_path = os.path.join(settings.MEDIA_ROOT, 'temp', os.path.basename(imagen_path))

                    with default_storage.open(imagen_full_path, 'rb') as imagen_file:
                        estudiante.avatar.save(os.path.basename(imagen_path), File(imagen_file), save=True)

                    default_storage.delete(imagen_full_path)

                request.session.flush()

                return redirect("list_estudiantes")
    else:
        initial_data = {}
        for key in request.session.keys():
            initial_data[key] = request.session[key]

        if 'dob' in initial_data and initial_data['dob']:
            initial_data['dob'] = datetime.strptime(initial_data['dob'], '%Y-%m-%d').date()

        if current_step == 1:
            form = EstudianteFormPasoUno(initial=initial_data)
        elif current_step == 2:
            form = EstudianteFormPasoDos(initial=initial_data)
        else:
            form = EstudianteFormPasoTres(initial=initial_data)

    submit_label = 'Siguiente Paso' if current_step < 3 else 'Crear Estudiante'

    session_data = request.session

    # Preparar datos para inicializar el formulario
    initial_data = {
        'nombre': session_data.get('nombre', ''),
        'email': session_data.get('email', ''),
        # Agrega aquí otros campos que necesites recuperar
        'dob': session_data.get('dob', None),
        'nivel_educativo': session_data.get('nivel_educativo', ''),
        'interest': session_data.get('interest', ''),
        'habilidades': session_data.get('habilidades', ''),
        'bio': session_data.get('bio', ''),
        'github': session_data.get('github', ''),
        'facebook': session_data.get('facebook', ''),
    }

    # Manejar la conversión de la fecha
    if initial_data['dob']:
        initial_data['dob'] = datetime.strptime(initial_data['dob'], '%Y-%m-%d').date()

    # Inicializar formularios con datos de la sesión
    if current_step == 1:
        form = EstudianteFormPasoUno(initial=initial_data)
    elif current_step == 2:
        form = EstudianteFormPasoDos(initial=initial_data)
    else:  # Paso 3
        form = EstudianteFormPasoTres(initial=initial_data)

    context = {
        'titulo': "Nuevo Estudiante",
        'form': form,
        'submit': submit_label,
        'previous_step': previous_step,
        'current_step': current_step,
        'next_step': next_step,
    }
    return render(request, "estudiante/estudiante_form.html", context)


def update_estudiante(request, estudiante_id):
    """
    Actualización de un estudiante
    """
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    if request.method == 'POST':
        form = EstudianteFormPasoUno(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect("list_estudiantes")
    else:
        form = EstudianteFormPasoUno(instance=estudiante)
    context = {
        'titulo': "Actualización de Estudiante",
        'form': form,
        'submit': 'Actualizar Estudiante'
    }
    return render(request, "estudiante/estudiante_form.html", context)