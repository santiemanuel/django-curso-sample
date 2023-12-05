from django.shortcuts import render, redirect
from ..models import Inscripcion, Estudiante
from ..forms.estudiante_form import BusquedaEstudianteForm
from ..forms.inscripcion_form import InscripcionForm

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