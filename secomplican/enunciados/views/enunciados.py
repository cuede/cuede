from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView

from enunciados import cuatrimestres_url_parser
from enunciados.models import Enunciado


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


class CrearEnunciado(CreateView):
    model = Enunciado
    fields = ['conjunto', 'numero']
