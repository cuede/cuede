from django.http import HttpResponse, HttpResponseBadRequest
from django.views import generic
from django.shortcuts import get_object_or_404, get_list_or_404, render

from enunciados import cuatrimestres_url_parser
from enunciados.models import Materia, Practica, Parcial, Enunciado
from enunciados import models_utils


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
    return render(request, 'enunciados/materia.html', contexto)


def practica(request, materia, anio, cuatrimestre, numero):
    numero_cuatri = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    if not numero_cuatri:
        return HttpResponseBadRequest('El cuatrimestre puede ser uno entre: "1cuatri", "2cuatri", "verano"')

    practica = get_object_or_404(Practica, materia__nombre=materia, cuatrimestre__anio=anio,
                                 cuatrimestre__numero=numero_cuatri,
                                 numero=numero)
    return render(request, 'enunciados/practica.html', {'practica': practica})


def parcial(request, materia, anio, cuatrimestre, numero, recuperatorio):
    numero_cuatri = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    if not numero_cuatri:
        return HttpResponseBadRequest('El cuatrimestre puede ser uno entre: "1cuatri", "2cuatri", "verano"')

    parcial = get_object_or_404(Parcial, materia__nombre=materia, cuatrimestre__anio=anio,
                                cuatrimestre__numero=numero_cuatri,
                                numero=numero, recuperatorio=recuperatorio)
    return render(request, 'enunciados/parcial.html', {'parcial': parcial})


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
    texto = enunciado_encontrado.versiones.ultima()
    return HttpResponse('{}'.format(texto))
