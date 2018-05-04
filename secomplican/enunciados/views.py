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

    contexto['parciales'] = models_utils.parciales_ordenados(contexto['materia'])
    return render(request, 'enunciados/materia.html', contexto)


def practica(request, materia, anio, cuatrimestre, numero):
    numero_cuatri = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    if not numero_cuatri:
        return HttpResponseBadRequest('El cuatrimestre puede ser uno entre: "1cuatri", "2cuatri", "verano"')

    practica = get_object_or_404(Practica, materia__nombre=materia, cuatrimestre__anio=anio,
                                 cuatrimestre__numero=numero_cuatri,
                                 numero=numero)
    return render(request, 'enunciados/practica.html', {'practica': practica})


def parcial(request, materia, anio, cuatrimestre, numero):
    numero_cuatri = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    if not numero_cuatri:
        return HttpResponseBadRequest('El cuatrimestre puede ser uno entre: "1cuatri", "2cuatri", "verano"')

    parcial = get_object_or_404(Parcial, materia__nombre=materia, cuatrimestre__anio=anio,
                                cuatrimestre__numero=numero_cuatri,
                                numero=numero, recuperatorio=False)
    return render(request, 'enunciados/parcial.html', {'parcial': parcial})


def enunciado(request, materia, anio, cuatrimestre, practica, numero):
    encontrado = get_list_or_404(Enunciado, practica__materia__nombre=materia)[0]
    return HttpResponse('{}'.format(encontrado))
