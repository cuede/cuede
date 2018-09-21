from django.http import Http404
from django.shortcuts import render, get_object_or_404

from enunciados.utils import cuatrimestres_url_parser, url_utils
from enunciados.models import Practica, Parcial, Final
from enunciados.utils.url_utils import add_query_params
from enunciados.views.enunciados.crear import ConjuntoDeEnunciadosForm
import datetime


def render_conjunto_de_enunciados(
        request, materia_carrera, conjunto, nuevo_enunciado_query_params):
    nuevo_enunciado_query_params['materia'] = materia_carrera.slug
    url_nuevo_enunciado = url_utils.reverse_con_queryparams(
        'agregar_enunciado', queryparams=nuevo_enunciado_query_params)
    contexto = {
        'carrera': materia_carrera.carrera,
        'conjunto': conjunto,
        'url_nuevo_enunciado': url_nuevo_enunciado,
    }
    return render(request, 'enunciados/conjunto_de_enunciados.html', contexto)


def conjunto_de_enunciados_con_cuatrimestre(
        request, queryset, anio, cuatrimestre, nuevo_enunciado_query_params):
    numero_cuatri = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    if not numero_cuatri:
        raise Http404

    conjunto = get_object_or_404(
        queryset, anio=anio, cuatrimestre=numero_cuatri)

    nuevo_enunciado_query_params['cuatrimestre'] = numero_cuatri
    nuevo_enunciado_query_params['anio'] = anio

    return render_conjunto_de_enunciados(
        request, conjunto, nuevo_enunciado_query_params)


def practica(request, materia, anio, cuatrimestre, numero):
    practicas = Practica.objects.filter(materia__slug=materia, numero=numero)
    nuevo_enunciado_query_params = {
        'tipo': ConjuntoDeEnunciadosForm.PRACTICA,
        'numero_practica': numero,
    }
    return conjunto_de_enunciados_con_cuatrimestre(
        request, practicas, anio, cuatrimestre, nuevo_enunciado_query_params)


def parcial(request, materia, anio, cuatrimestre, numero, recuperatorio=False):
    parciales = Parcial.objects.filter(
        materia__slug=materia, numero=numero, recuperatorio=recuperatorio)
    nuevo_enunciado_query_params = {
        'tipo': ConjuntoDeEnunciadosForm.PARCIAL,
        'numero_parcial': numero,
        'es_recuperatorio': recuperatorio,
    }
    return conjunto_de_enunciados_con_cuatrimestre(
        request, parciales, anio, cuatrimestre, nuevo_enunciado_query_params)


def final(request, materia_carrera, fecha):
    final_encontrado = get_object_or_404(
        Final, materia=materia_carrera.materia, fecha=fecha)

    nuevo_enunciado_query_params = {
        'tipo': ConjuntoDeEnunciadosForm.FINAL,
        'fecha': fecha,
    }
    return render_conjunto_de_enunciados(
        request, materia_carrera,
        final_encontrado, nuevo_enunciado_query_params)
