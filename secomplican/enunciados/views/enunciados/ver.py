from django.shortcuts import render
from django.urls import reverse

from enunciados.utils import cuatrimestres_url_parser

from . import enunciados_utils


def render_enunciado(
        request, enunciado_elegido, url_solucion, url_editar, conjunto):
    contexto = {
        'enunciado': enunciado_elegido,
        'url_solucion': url_solucion,
        'url_editar': url_editar,
        'conjunto': conjunto,
    }
    return render(request, 'enunciados/enunciado.html', contexto)


def enunciado_practica(request, materia, anio, cuatrimestre, numero_practica, numero):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = enunciados_utils.enunciado_de_practica(
        materia, anio, numero_cuatrimestre, numero_practica, numero)
    url_solucion = reverse('solucion_practica', kwargs={
        'materia': materia, 'anio': anio, 'cuatrimestre': cuatrimestre,
        'numero_practica': numero_practica,
        'numero': numero,
    })
    url_editar = reverse('editar_enunciado_practica', kwargs={
        'materia': materia, 'anio': anio, 'cuatrimestre': cuatrimestre,
        'numero_practica': numero_practica,
        'numero': numero,
    })
    conjunto = encontrado.conjunto.practica
    return render_enunciado(
        request, encontrado, url_solucion, url_editar, conjunto)


def enunciado_parcial(request, materia, anio, cuatrimestre, numero_parcial, numero, es_recuperatorio):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = enunciados_utils.enunciado_de_parcial(
        materia, anio, numero_cuatrimestre, numero_parcial, numero, es_recuperatorio)
    if es_recuperatorio:
        nombre_url_solucion = 'solucion_recuperatorio'
        nombre_url_editar = 'editar_enunciado_recuperatorio'
    else:
        nombre_url_solucion = 'solucion_parcial'
        nombre_url_editar = 'editar_enunciado_parcial'

    url_solucion = reverse(nombre_url_solucion, kwargs={
        'materia': materia, 'anio': anio, 'cuatrimestre': cuatrimestre,
        'numero_parcial': numero_parcial, 'numero': numero
    })
    url_editar = reverse(nombre_url_editar, kwargs={
        'materia': materia, 'anio': anio, 'cuatrimestre': cuatrimestre,
        'numero_parcial': numero_parcial, 'numero': numero
    })
    conjunto = encontrado.conjunto.parcial
    return render_enunciado(
        request, encontrado, url_solucion, url_editar, conjunto)


def enunciado_final(request, materia, anio, mes, dia, numero):
    encontrado = enunciados_utils.enunciado_de_final(
        materia, anio, mes, dia, numero)
    url_solucion = reverse('solucion_final', kwargs={
        'materia': materia, 'anio': anio, 'mes': mes, 'dia': dia,
        'numero': numero,
    })
    url_solucion = reverse('editar_enunciado_final', kwargs={
        'materia': materia, 'anio': anio, 'mes': mes, 'dia': dia,
        'numero': numero
    })
    conjunto = encontrado.conjunto.final
    return render_enunciado(
        request, encontrado, url_solucion, url_editar, conjunto)
