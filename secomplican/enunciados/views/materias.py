from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from enunciados.models import MateriaCarrera
from enunciados.utils import models_utils, url_utils
from enunciados.views.enunciados.forms import ConjuntoDeEnunciadosForm


class MateriasView(generic.ListView):
    model = MateriaCarrera
    template_name = 'enunciados/materias.html'


def url_agregar_conjunto(slug_materia, tipo):
    queryparams = {
        'materia': slug_materia,
        'tipo': tipo,
    }
    return url_utils.reverse_con_queryparams(
        'agregar_enunciado', queryparams=queryparams)


def materia(request, materia_carrera):
    tipo_practica = ConjuntoDeEnunciadosForm.PRACTICA
    tipo_parcial = ConjuntoDeEnunciadosForm.PARCIAL
    tipo_final = ConjuntoDeEnunciadosForm.FINAL
    contexto = {
        'materia': materia_carrera,
        'practicas': models_utils.ultimas_practicas_ordenadas(
            materia_carrera.materia),
        'parciales': models_utils.parciales_de_materia_ordenados(
            materia_carrera.materia),
        'finales': models_utils.finales_de_materia_ordenados(
            materia_carrera.materia),

        'url_agregar_practica': url_agregar_conjunto(
            materia_carrera.slug, tipo_practica),
        'url_agregar_parcial': url_agregar_conjunto(
            materia_carrera.slug, tipo_parcial),
        'url_agregar_final': url_agregar_conjunto(
            materia_carrera.slug, tipo_final),
    }
    return render(request, 'enunciados/materia.html', contexto)
