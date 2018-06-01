from django.shortcuts import get_object_or_404, render
from django.views import generic

from enunciados import models_utils, cuatrimestres_url_parser
from enunciados.models import Materia


class MateriasView(generic.ListView):
    model = Materia


def materia(request, nombre):
    contexto = {
        'materia': get_object_or_404(Materia, nombre=nombre),
    }
    contexto['practicas'] = models_utils.ultimas_practicas_ordenadas(contexto['materia'])
    if contexto['practicas']:
        ultimo_cuatrimestre = contexto['practicas'][0].cuatrimestre
        contexto['url_cuatrimestre_practicas'] = cuatrimestres_url_parser.numero_a_url(ultimo_cuatrimestre.numero)
        contexto['ultimo_anio_practicas'] = ultimo_cuatrimestre.anio

    contexto['parciales'] = models_utils.parciales_de_materia_ordenados(contexto['materia'])
    contexto['finales'] = models_utils.finales_de_materia_ordenados(contexto['materia'])
    return render(request, 'enunciados/materia.html', contexto)