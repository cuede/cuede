from django.shortcuts import get_object_or_404, render
from django.views import generic

from enunciados import models_utils
from enunciados.models import Materia


class MateriasView(generic.ListView):
    model = Materia


def materia(request, nombre):
    # El nombre es un slug.
    contexto = {
        'materia': get_object_or_404(Materia, slug=nombre),
    }
    contexto['practicas'] = models_utils.ultimas_practicas_ordenadas(contexto['materia'])
    contexto['parciales'] = models_utils.parciales_de_materia_ordenados(contexto['materia'])
    contexto['finales'] = models_utils.finales_de_materia_ordenados(contexto['materia'])
    return render(request, 'enunciados/materia.html', contexto)
