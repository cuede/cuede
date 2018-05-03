from django.http import HttpResponse
from django.views import generic
from django.shortcuts import get_object_or_404, get_list_or_404, render
from enunciados.models import Materia, Enunciado


def index(request):
    return HttpResponse("Se complican :)")


class MateriasView(generic.ListView):
    model = Materia


def materia(request, nombre):
    objeto = get_object_or_404(Materia, nombre=nombre)
    return render(request, 'enunciados/materia.html', {'materia': objeto})


def enunciado(request, materia, cuatrimestre, practica, numero):
    encontrado = get_list_or_404(Enunciado, practica__materia__nombre=materia)[0]
    return HttpResponse('{}'.format(encontrado))
