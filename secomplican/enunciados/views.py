from django.http import HttpResponse
from django.views import generic
from django.db.models import Count
from django.shortcuts import get_list_or_404
from enunciados.models import Materia, Etapa, Practica, Enunciado
import enunciados.models_utils as models_utils


def index(request):
    return HttpResponse("Se complican :)")


class MateriasView(generic.ListView):
    model = Materia


class EtapasView(generic.ListView):
    model = Etapa
    # Por alguna razon si de get_queryset devolvemos algo que no sea un QuerySet pero si un iterable,
    # tenemos que especificar el template_name aca, o el template engine rompe.
    template_name = 'enunciados/etapa_list.html'

    def get_queryset(self):
        # queremos las etapas que tengan por lo menos una practica
        # de la materia.
        materia = self.kwargs['materia']
        # Sacamos las etapas que ya sabemos que no tienen practicas
        etapas = Etapa.objects.annotate(cant_practicas=Count('practica')).filter(cant_practicas__gt=0)
        # Filtramos por las que tienen alguna practica de la materia
        etapas_filtradas = [etapa for etapa in etapas if models_utils.tiene_practica_con_materia(etapa, materia)]
        return etapas_filtradas


def enunciado(request, materia, etapa, practica, numero):
    encontrado = get_list_or_404(Enunciado, practica__materia__nombre=materia)[0]
    return HttpResponse('{}'.format(encontrado))
