from django.shortcuts import get_object_or_404
from django.http import Http404

from enunciados.models import Enunciado
from enunciados.utils import cuatrimestres_url_parser


def enunciado_con_kwargs(kwargs):
    materia = kwargs.get('materia')
    anio = kwargs.get('anio')
    numero = kwargs.get('numero')
    conjunto = kwargs.get('conjunto')
    if conjunto == 'final':
        mes = kwargs.get('mes')
        dia = kwargs.get('dia')
        return enunciado_de_final(materia, anio, mes, dia, numero)
    else:
        cuatrimestre = kwargs.get('cuatrimestre')
        numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(
            cuatrimestre)
        if conjunto == 'practica':
            numero_practica = kwargs.get('numero_practica')
            return enunciado_de_practica(
                materia, anio, numero_cuatrimestre, numero_practica, numero)
        elif conjunto == 'parcial':
            numero_parcial = kwargs.get('numero_parcial')
            es_recuperatorio = kwargs.get('es_recuperatorio', False)
            return enunciado_de_parcial(
                materia, anio, numero_cuatrimestre,
                numero_parcial, numero, es_recuperatorio)
        else:
            raise Http404('El enunciado no tiene un conjunto válido.')


def enunciado_de_practica(materia, anio, numero_cuatrimestre, numero_practica, numero):
    return get_object_or_404(
        Enunciado,
        conjunto__materia__slug=materia,
        numero=numero,
        conjunto__practica__isnull=False,
        conjunto__practica__anio=anio,
        conjunto__practica__cuatrimestre=numero_cuatrimestre,
        conjunto__practica__numero=numero_practica,
    )


def enunciado_de_parcial(materia, anio, numero_cuatrimestre, numero_parcial, numero, es_recuperatorio):
    return get_object_or_404(
        Enunciado,
        conjunto__materia__slug=materia,
        numero=numero,
        conjunto__parcial__isnull=False,
        conjunto__parcial__anio=anio,
        conjunto__parcial__cuatrimestre=numero_cuatrimestre,
        conjunto__parcial__numero=numero_parcial,
        conjunto__parcial__recuperatorio=es_recuperatorio,
    )


def enunciado_de_final(materia, anio, mes, dia, numero):
    return get_object_or_404(
        Enunciado,
        conjunto__materia__slug=materia,
        numero=numero,
        conjunto__final__isnull=False,
        conjunto__final__fecha__year=anio,
        conjunto__final__fecha__month=mes,
        conjunto__final__fecha__day=dia,
    )
