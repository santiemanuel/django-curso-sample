from django.shortcuts import render, HttpResponse
from .models import Curso


def all_courses(request):
    cursos = Curso.objects.all()
    html_output = f"<p>"
    for i, curso in enumerate(cursos):
        html_output += f"<h1>{curso.nombre}</h1><p>{i+1}{curso.descripcion}</p>"
    return HttpResponse(html_output)


def premium_courses(request):
    pass


def next_year_courses(request):
    pass
