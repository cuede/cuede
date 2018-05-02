from django.http import HttpResponse
from django.views import generic
from enunciados.models import Materia, Enunciado
from django.shortcuts import get_list_or_404


def index(request):
    return HttpResponse("Se complican :)")


class MateriasView(generic.ListView):
    model = Materia


def enunciado(request, materia, etapa, practica, numero):
    encontrado = get_list_or_404(Enunciado, practica__materia__nombre=materia)[0]
    return HttpResponse('{}'.format(encontrado))
