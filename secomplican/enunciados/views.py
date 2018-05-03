from django.http import HttpResponse, HttpResponseBadRequest
from django.views import generic
from django.shortcuts import get_object_or_404, get_list_or_404, render
from enunciados.models import Materia, Cuatrimestre, Practica, Enunciado


def index(request):
    return HttpResponse("QED.com.ar: donde tooodos te piden que la demuestres.")


class MateriasView(generic.ListView):
    model = Materia


def materia(request, nombre):
    objeto = get_object_or_404(Materia, nombre=nombre)
    return render(request, 'enunciados/materia.html', {'materia': objeto})


def __parsear_cuatrimestre(cuatrimestre):
    """
    Devuelve el numero de cuatrimestre parseando el parámetro de una url.

    :returns: None si es que cuatrimestre no es uno entre '1cuatri', '2cuatri' o 'verano'
    """
    if cuatrimestre == '1cuatri':
        return Cuatrimestre.PRIMERO
    elif cuatrimestre == '2cuatri':
        return Cuatrimestre.SEGUNDO
    elif cuatrimestre == 'verano':
        return Cuatrimestre.VERANO
    else:
        return None


def practica(request, materia, anio, cuatrimestre, numero):
    numero_cuatri = __parsear_cuatrimestre(cuatrimestre)
    if not numero_cuatri:
        return HttpResponseBadRequest('El cuatrimestre puede ser uno entre: "1cuatri", "2cuatri", "verano"')

    practica = get_object_or_404(Practica, materia__nombre=materia, cuatrimestre__anio=anio,
                                 cuatrimestre__cuatrimestre=numero_cuatri,
                                 numero=numero)
    return render(request, 'enunciados/practica.html', {'practica': practica})


def enunciado(request, materia, anio, cuatrimestre, practica, numero):
    encontrado = get_list_or_404(Enunciado, practica__materia__nombre=materia)[0]
    return HttpResponse('{}'.format(encontrado))
