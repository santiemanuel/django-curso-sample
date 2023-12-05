from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..models import Estudiante
from ..forms.estudiante_form import EstudianteForm

from django.contrib.auth import get_user_model

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