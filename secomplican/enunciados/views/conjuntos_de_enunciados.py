from django.shortcuts import render
from django.urls import reverse
from enunciados.utils import conjuntos_url_parser, enunciados_url_parser


def conjunto_de_enunciados(request, **kwargs):
    materia_carrera = kwargs['materia_carrera']
    conjunto = conjuntos_url_parser.kwargs_a_conjunto(kwargs)
    url_nuevo_enunciado = enunciados_url_parser.url_nuevo_enunciado(
        materia_carrera, conjunto)
    contexto = {
        'carrera': materia_carrera.carrera,
        'materia_carrera': materia_carrera,
        'conjunto': conjunto,
        'url_nuevo_enunciado': url_nuevo_enunciado,
    }
    return render(request, 'enunciados/conjunto_de_enunciados.html', contexto)
