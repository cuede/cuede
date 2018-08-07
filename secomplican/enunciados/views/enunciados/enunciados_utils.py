from django.shortcuts import get_object_or_404

from enunciados.models import Enunciado


def enunciado_de_practica(materia, anio, numero_cuatrimestre, numero_practica, numero):
    return get_object_or_404(
        Enunciado,
        conjunto__materia__nombre=materia,
        numero=numero,
        conjunto__practica__isnull=False,
        conjunto__practica__cuatrimestre__anio=anio,
        conjunto__practica__cuatrimestre__numero=numero_cuatrimestre,
        conjunto__practica__numero=numero_practica,
    )


def enunciado_de_parcial(materia, anio, numero_cuatrimestre, numero_parcial, numero, es_recuperatorio):
    return get_object_or_404(
            Enunciado,
            conjunto__materia__nombre=materia,
            numero=numero,
            conjunto__parcial__isnull=False,
            conjunto__parcial__cuatrimestre__anio=anio,
            conjunto__parcial__cuatrimestre__numero=numero_cuatrimestre,
            conjunto__parcial__numero=numero_parcial,
            conjunto__parcial__recuperatorio=es_recuperatorio,
        )


def enunciado_de_final(materia, anio, mes, dia, numero):
    return get_object_or_404(
        Enunciado,
        conjunto__materia__nombre=materia,
        numero=numero,
        conjunto__final__isnull=False,
        conjunto__final__fecha__year=anio,
        conjunto__final__fecha__month=mes,
        conjunto__final__fecha__day=dia,
    )