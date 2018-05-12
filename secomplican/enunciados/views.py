from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic

from enunciados import cuatrimestres_url_parser
from enunciados import models_utils
from enunciados.models import Materia, Practica, Parcial, Final, Enunciado


def index(request):
    return HttpResponse(
        '<h1>QED.com.ar: donde tooodos te piden que la demuestres.</h1><a href="/materias">Materias</a>')


class MateriasView(generic.ListView):
    model = Materia


def materia(request, nombre):
    contexto = {
        'materia': get_object_or_404(Materia, nombre=nombre),
    }
    contexto['practicas'] = models_utils.ultimas_practicas_ordenadas(contexto['materia'])
    if contexto['practicas']:
        ultimo_cuatrimestre = contexto['practicas'][0].cuatrimestre
        contexto['url_cuatrimestre_practicas'] = cuatrimestres_url_parser.numero_a_url(ultimo_cuatrimestre.numero)
        contexto['ultimo_anio_practicas'] = ultimo_cuatrimestre.anio

    contexto['parciales'] = models_utils.parciales_de_materia_ordenados(contexto['materia'])
    contexto['finales'] = models_utils.finales_de_materia_ordenados(contexto['materia'])
    return render(request, 'enunciados/materia.html', contexto)


def render_conjunto_de_enunciados(request, conjunto):
    return render(request, 'enunciados/conjunto_de_enunciados.html', {'conjunto': conjunto})


def conjunto_de_enunciados_con_cuatrimestre(request, queryset, anio, cuatrimestre):
    numero_cuatri = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    if not numero_cuatri:
        raise Http404

    conjunto = get_object_or_404(queryset, cuatrimestre__anio=anio, cuatrimestre__numero=numero_cuatri)

    return render_conjunto_de_enunciados(request, conjunto)


def practica(request, materia, anio, cuatrimestre, numero):
    practicas = Practica.objects.filter(materia__nombre=materia, numero=numero)
    return conjunto_de_enunciados_con_cuatrimestre(request, practicas, anio, cuatrimestre)


def parcial(request, materia, anio, cuatrimestre, numero, recuperatorio=False):
    parciales = Parcial.objects.filter(materia__nombre=materia, numero=numero, recuperatorio=recuperatorio)
    return conjunto_de_enunciados_con_cuatrimestre(request, parciales, anio, cuatrimestre)


def final(request, materia, anio, mes, dia):
    finales = get_object_or_404(Final, materia__nombre=materia, fecha__year=anio, fecha__month=mes, fecha__day=dia)
    return render_conjunto_de_enunciados(request, finales)


def render_enunciado(enunciado_elegido):
    return HttpResponse('{}'.format(enunciado_elegido.versiones.ultima()))


def enunciado(request, materia, anio, cuatrimestre, conjunto_de_enunciados, tipo_conjunto, numero):
    encontrados = Enunciado.objects.filter(
        conjunto__materia__nombre=materia,
        conjunto__cuatrimestre__anio=anio,
        conjunto__cuatrimestre__numero=cuatrimestres_url_parser.url_a_numero(cuatrimestre),
        numero=numero,
    )
    if tipo_conjunto == 'practica':
        encontrados = encontrados.filter(conjunto__practica__isnull=False) \
            .filter(conjunto__practica__numero=conjunto_de_enunciados)
    else:
        encontrados = encontrados.filter(conjunto__parcial__isnull=False)
        es_recuperatorio = tipo_conjunto == 'recuperatorio'
        encontrados = encontrados.filter(conjunto__parcial__recuperatorio=es_recuperatorio) \
            .filter(conjunto__parcial__numero=conjunto_de_enunciados)

    enunciado_encontrado = encontrados[0]
    return render_enunciado(enunciado_encontrado)


def enunciado_final(request, materia, anio, mes, dia, numero):
    encontrado = get_object_or_404(
        Enunciado,
        conjunto__materia__nombre=materia,
        numero=numero,
        conjunto__final__isnull=False,
        conjunto__final__fecha__year=anio,
        conjunto__final__fecha__month=mes,
        conjunto__final__fecha__day=dia,
    )

    return render_enunciado(encontrado)
