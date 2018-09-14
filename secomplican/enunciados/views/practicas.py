from itertools import groupby
from django.shortcuts import get_object_or_404, render


from enunciados.models import Practica, Materia
from enunciados.utils import cuatrimestres_parser


def cuatrimestre_y_anio_a_texto(conjunto):
    texto_cuatrimestre = cuatrimestres_parser.numero_a_texto(
        conjunto.cuatrimestre)
    return '{} del {}'.format(texto_cuatrimestre, conjunto.anio)


def practicas_de_materia(materia):
    practicas = (Practica.objects
        .filter(materia=materia)
        .order_by('-anio', '-cuatrimestre', 'numero')
    )
    agrupadas = groupby(practicas, key=cuatrimestre_y_anio_a_texto)
    retornables = {}
    for cuatri, practicas_de_cuatri in agrupadas:
        retornables[cuatri] = list(practicas_de_cuatri)
    return retornables


def practicas(request, materia_carrera):
    practicas_materia = practicas_de_materia(materia_carrera.materia)
    return render(
        request, 'enunciados/practicas.html', {'practicas': practicas_materia}
    )