from django.shortcuts import render
from django.urls import reverse

from enunciados.utils import (
    enunciados_url_parser, cuatrimestres_url_parser,
    soluciones_url_parser, conjuntos_utils)


def render_enunciado(request, materia_carrera,
                     enunciado_elegido, url_agregar_solucion, conjunto):
    contexto = {
        'carrera': materia_carrera.carrera,
        'materia_carrera': materia_carrera,
        'enunciado': enunciado_elegido,
        'url_agregar_solucion': url_agregar_solucion,
        'conjunto': conjunto,
    }
    return render(request, 'enunciados/enunciado.html', contexto)


def enunciado(request, **kwargs):
    enunciado_encontrado = enunciados_url_parser.kwargs_a_enunciado(kwargs)
    tipo_conjunto = conjuntos_utils.tipo_conjunto(
        enunciado_encontrado.conjunto)
    conjunto = enunciado_encontrado.conjunto
    if tipo_conjunto == 'practica':
        conjunto = conjunto.practica
    elif tipo_conjunto == 'parcial':
        conjunto = conjunto.parcial
    elif tipo_conjunto == 'final':
        conjunto = conjunto.final

    materia_carrera = kwargs.get('materia_carrera')
    url_agregar_solucion = soluciones_url_parser.url_nueva_solucion(
        materia_carrera, enunciado_encontrado)
    return render_enunciado(
        request, materia_carrera,
        enunciado_encontrado, url_agregar_solucion, conjunto)
