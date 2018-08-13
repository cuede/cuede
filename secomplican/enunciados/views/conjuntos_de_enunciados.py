from django.http import Http404
from django.shortcuts import render, get_object_or_404

from enunciados import cuatrimestres_url_parser
from enunciados.models import Practica, Parcial, Final


def render_conjunto_de_enunciados(request, conjunto):
    return render(request, 'enunciados/conjunto_de_enunciados.html', {'conjunto': conjunto})


def conjunto_de_enunciados_con_cuatrimestre(request, queryset, anio, cuatrimestre):
    numero_cuatri = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    if not numero_cuatri:
        raise Http404

    conjunto = get_object_or_404(queryset, anio=anio, cuatrimestre=numero_cuatri)

    return render_conjunto_de_enunciados(request, conjunto)


def practica(request, materia, anio, cuatrimestre, numero):
    practicas = Practica.objects.filter(materia__slug=materia, numero=numero)
    return conjunto_de_enunciados_con_cuatrimestre(request, practicas, anio, cuatrimestre)


def parcial(request, materia, anio, cuatrimestre, numero, recuperatorio=False):
    parciales = Parcial.objects.filter(materia__slug=materia, numero=numero, recuperatorio=recuperatorio)
    return conjunto_de_enunciados_con_cuatrimestre(request, parciales, anio, cuatrimestre)


def final(request, materia, anio, mes, dia):
    finales = get_object_or_404(Final, materia__slug=materia, fecha__year=anio, fecha__month=mes, fecha__day=dia)
    return render_conjunto_de_enunciados(request, finales)
