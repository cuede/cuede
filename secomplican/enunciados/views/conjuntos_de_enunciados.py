from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from enunciados.utils import cuatrimestres_url_parser
from enunciados.models import Practica, Parcial, Final
from enunciados.utils.url_utils import add_query_params
from enunciados.views.enunciados.crear import ConjuntoDeEnunciadosForm
import datetime


def render_conjunto_de_enunciados(
        request, conjunto, nuevo_enunciado_query_params):
    url_nuevo_enunciado = reverse(
        'agregar_enunciado', kwargs={'materia': conjunto.materia.slug})
    url_nuevo_enunciado_con_params = add_query_params(
        url_nuevo_enunciado, **nuevo_enunciado_query_params)
    contexto = {'conjunto': conjunto,
                'url_nuevo_enunciado': url_nuevo_enunciado_con_params}
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


def final(request, materia, anio, mes, dia):
    finales = get_object_or_404(
        Final, materia__slug=materia,
        fecha__year=anio, fecha__month=mes, fecha__day=dia)

    fecha = datetime.date(anio, mes, dia)
    nuevo_enunciado_query_params = {
        'tipo': ConjuntoDeEnunciadosForm.FINAL,
        'fecha': fecha,
    }
    return render_conjunto_de_enunciados(
        request, finales, nuevo_enunciado_query_params)
