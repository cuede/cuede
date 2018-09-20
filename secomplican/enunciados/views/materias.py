from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from enunciados.models import MateriaCarrera
from enunciados.utils import models_utils, url_utils, conjuntos_url_parser
from enunciados.views.enunciados.forms import ConjuntoDeEnunciadosForm


class MateriasView(generic.ListView):
    model = MateriaCarrera
    template_name = 'enunciados/materias.html'

    def get_queryset(self):
        carrera = self.kwargs.get('carrera')
        return super().get_queryset().filter(carrera=carrera)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carrera'] = self.kwargs.get('carrera')
        return context


def url_agregar_conjunto(slug_materia, tipo):
    queryparams = {
        'materia': slug_materia,
        'tipo': tipo,
    }
    return url_utils.reverse_con_queryparams(
        'agregar_enunciado', queryparams=queryparams)


def practicas_con_urls(materiacarrera):
    practicas = models_utils.ultimas_practicas_ordenadas(
        materiacarrera.materia)
    return [
        (practica, conjuntos_url_parser.url_practica(materiacarrera, practica))
        for practica in practicas
    ]


def parciales_con_urls(materiacarrera):
    parciales_por_numero = models_utils.parciales_de_materia_ordenados(
        materiacarrera.materia)
    for numero, parciales in parciales_por_numero.items():
        parciales_por_numero[numero] = [
            (parcial, conjuntos_url_parser.url_parcial(materiacarrera, parcial))
            for parcial in parciales
        ]
    return parciales_por_numero


def materia(request, materia_carrera):
    tipo_practica = ConjuntoDeEnunciadosForm.PRACTICA
    tipo_parcial = ConjuntoDeEnunciadosForm.PARCIAL
    tipo_final = ConjuntoDeEnunciadosForm.FINAL

    # Pasar las URLs de practicas, parciales y finales.
    # Hay que hacer tipo un zip para poder recorrer los parciales
    # y sus URLs al mismo tiempo.
    contexto = {
        'carrera': materia_carrera.carrera,
        'materia': materia_carrera,
        'practicas_con_urls': practicas_con_urls(materia_carrera),
        'parciales_con_urls': parciales_con_urls(materia_carrera),
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
