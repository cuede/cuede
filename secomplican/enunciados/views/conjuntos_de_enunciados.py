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
        'materia_carrera': materia_carrera,
        'conjunto': conjunto,
        'url_nuevo_enunciado': url_nuevo_enunciado,
    }
    return render(request, 'enunciados/conjunto_de_enunciados.html', contexto)


def conjunto_de_enunciados_con_cuatrimestre(
        request, materia_carrera, queryset,
        anio, cuatrimestre, nuevo_enunciado_query_params):

    conjunto = get_object_or_404(
        queryset, anio=anio, cuatrimestre=cuatrimestre)

    nuevo_enunciado_query_params['cuatrimestre'] = cuatrimestre
    nuevo_enunciado_query_params['anio'] = anio

    return render_conjunto_de_enunciados(
        request, materia_carrera, conjunto, nuevo_enunciado_query_params)


def practica(request, materia_carrera, anio, cuatrimestre, numero_practica):
    practicas = Practica.objects.filter(
        materia=materia_carrera.materia, numero=numero_practica)
    nuevo_enunciado_query_params = {
        'tipo': ConjuntoDeEnunciadosForm.PRACTICA,
        'numero_practica': numero_practica,
    }
    return conjunto_de_enunciados_con_cuatrimestre(
        request, materia_carrera, practicas,
        anio, cuatrimestre, nuevo_enunciado_query_params)


def parcial(
        request, materia_carrera, anio,
        cuatrimestre, numero_parcial, recuperatorio=False):
    parciales = Parcial.objects.filter(
        materia=materia_carrera.materia,
        numero=numero_parcial,
        recuperatorio=recuperatorio)
    nuevo_enunciado_query_params = {
        'tipo': ConjuntoDeEnunciadosForm.PARCIAL,
        'numero_parcial': numero_parcial,
        'es_recuperatorio': recuperatorio,
    }
    return conjunto_de_enunciados_con_cuatrimestre(
        request, materia_carrera, parciales,
        anio, cuatrimestre, nuevo_enunciado_query_params)


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
