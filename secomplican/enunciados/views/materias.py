from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from enunciados.models import Materia
from enunciados.utils import models_utils, url_utils
from enunciados.views.enunciados.forms import ConjuntoDeEnunciadosForm


class MateriasView(generic.ListView):
    model = Materia


def url_agregar_conjunto(slug_materia, tipo):
    url = reverse('agregar_enunciado', kwargs={'materia': slug_materia})
    return url_utils.add_query_params(url, tipo=tipo)


def materia(request, nombre):
    # El nombre es un slug.
    materia_encontrada = get_object_or_404(Materia, slug=nombre)
    tipo_practica = ConjuntoDeEnunciadosForm.PRACTICA
    tipo_parcial = ConjuntoDeEnunciadosForm.PARCIAL
    tipo_final = ConjuntoDeEnunciadosForm.FINAL
    contexto = {
        'materia': materia_encontrada,
        'practicas': models_utils.ultimas_practicas_ordenadas(
            materia_encontrada),
        'parciales': models_utils.parciales_de_materia_ordenados(
            materia_encontrada),
        'finales': models_utils.finales_de_materia_ordenados(
            materia_encontrada),

        'url_agregar_practica': url_agregar_conjunto(nombre, tipo_practica),
        'url_agregar_parcial': url_agregar_conjunto(nombre, tipo_parcial),
        'url_agregar_final': url_agregar_conjunto(nombre, tipo_final),
    }
    return render(request, 'enunciados/materia.html', contexto)
