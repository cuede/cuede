from django.shortcuts import render
from django.urls import reverse

from enunciados.utils import (
    enunciados_url_parser, cuatrimestres_url_parser,
    soluciones_url_parser, conjuntos_utils)
from enunciados.views.breadcrumb import breadcrumb_ver_enunciado
from enunciados.models import Voto


def voto_de_solucion(usuario, solucion):
    if usuario.is_authenticated:
        return Voto.objects.filter(solucion=solucion, usuario=usuario.informacionusuario).first()
    else:
        return None


def enunciado(request, **kwargs):
    enunciado_encontrado = enunciados_url_parser.kwargs_a_enunciado(kwargs)
    tipo_conjunto = conjuntos_utils.tipo_conjunto(
        enunciado_encontrado.conjunto)
    conjunto = enunciado_encontrado.conjunto
    if tipo_conjunto == 'practica':
        conjunto = conjunto.practica
    elif tipo_conjunto == 'parcial':
        conjunto = conjunto.parcial
    elif tipo_conjunto == 'final':
        conjunto = conjunto.final

    materia_carrera = kwargs.get('materia_carrera')
    url_agregar_solucion = soluciones_url_parser.url_nueva_solucion(
        materia_carrera, enunciado_encontrado)

    soluciones = enunciado_encontrado.soluciones.order_by('-puntos')

    soluciones_con_votos = [
        (solucion, voto_de_solucion(request.user, solucion))
        for solucion in soluciones
    ]

    contexto = {
        'carrera': materia_carrera.carrera,
        'materia_carrera': materia_carrera,
        'enunciado': enunciado_encontrado,
        'url_agregar_solucion': url_agregar_solucion,
        'conjunto': conjunto,
        'breadcrumb': breadcrumb_ver_enunciado(
            materia_carrera, enunciado_encontrado),
        'soluciones_con_votos': soluciones_con_votos,
        'usuario_logueado': request.user.is_authenticated,
    }
    return render(request, 'enunciados/enunciado.html', contexto)