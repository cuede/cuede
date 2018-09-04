from django.shortcuts import render, redirect, get_object_or_404

from enunciados.models import Enunciado
from enunciados.utils import cuatrimestres_url_parser
from . import enunciados_utils


def volver_a_version(enunciado, pk):
    version = get_object_or_404(enunciado.versiones, pk=pk)
    version.pk = None
    version.save()


def render_enunciado(request, enunciado, conjunto):
    if request.method == 'POST':
        # Nos postearon una versión a la que volver.
        # La versión está en version_pk.
        pk = request.POST.get('version_pk')
        if pk:
            volver_a_version(enunciado, pk)
            return redirect(enunciado)

    contexto = {
        'enunciado': enunciado,
        'conjunto': conjunto,
    }
    return render(request, 'enunciados/versiones_enunciado.html', contexto)


def enunciado_practica(
    request, materia, anio, cuatrimestre, numero_practica, numero):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = enunciados_utils.enunciado_de_practica(
        materia, anio, numero_cuatrimestre, numero_practica, numero)
    return render_enunciado(request, encontrado, encontrado.conjunto.practica)


def enunciado_parcial(request, materia, anio, cuatrimestre,
    numero_parcial, numero, es_recuperatorio=False):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = enunciados_utils.enunciado_de_parcial(
        materia, anio, numero_cuatrimestre, numero_parcial,
        numero, es_recuperatorio)
    return render_enunciado(request, encontrado, encontrado.conjunto.parcial)


def enunciado_final(request, materia, anio, mes, dia):
    encontrado = enunciados_utils.enunciado_de_final(
        materia, anio, mes, dia, numero)
    return render_enunciado(request, encontrado, encontrado.conjunto.final)
