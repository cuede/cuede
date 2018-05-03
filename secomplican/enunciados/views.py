from django.http import HttpResponse
from django.views import generic
from django.db.models import Count
from django.shortcuts import get_object_or_404, get_list_or_404, render
from enunciados.models import Materia, Cuatrimestre, Practica, Enunciado
import enunciados.models_utils as models_utils


def index(request):
    return HttpResponse("Se complican :)")


class MateriasView(generic.ListView):
    model = Materia


def materia(request, nombre):
    objeto = get_object_or_404(Materia, nombre=nombre)
    return render(request, 'enunciados/materia.html', {'materia': objeto})


class CuatrimestreView(generic.ListView):
    model = Cuatrimestre
    # Por alguna razon si de get_queryset devolvemos algo que no sea un QuerySet pero si un iterable,
    # tenemos que especificar el template_name aca, o el template engine rompe.
    template_name = 'enunciados/cuatrimestre_list.html'

    def get_queryset(self):
        # queremos los cuatrimestres que tengan por lo menos una practica
        # de la materia.
        materia = self.kwargs['materia']
        # Sacamos los cuatrimestres que ya sabemos que no tienen practicas
        cuatrimestres = Cuatrimestre.objects.annotate(cant_practicas=Count('practica')).filter(cant_practicas__gt=0)
        # Filtramos por los que tienen alguna practica de la materia
        cuatrimestres_filtrados = [cuatrimestre for cuatrimestre in cuatrimestres
                            if models_utils.tiene_practica_con_materia(cuatrimestre, materia)]
        return cuatrimestres_filtrados


def enunciado(request, materia, cuatrimestre, practica, numero):
    encontrado = get_list_or_404(Enunciado, practica__materia__nombre=materia)[0]
    return HttpResponse('{}'.format(encontrado))
