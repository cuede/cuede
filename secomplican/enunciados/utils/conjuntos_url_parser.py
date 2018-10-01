from django.shortcuts import get_object_or_404
from django.urls import reverse

from enunciados.utils import cuatrimestres_url_parser, conjuntos_utils
from enunciados.models import Practica, Parcial, Final


def _kwargs_de_conjunto_con_cuatrimestre(conjunto):
    return {
        'anio': conjunto.anio,
        'cuatrimestre': conjunto.cuatrimestre,
    }


def kwargs_de_practica(practica):
    kwargs = _kwargs_de_conjunto_con_cuatrimestre(practica)
    kwargs['numero_practica'] = practica.numero
    return kwargs


def kwargs_de_parcial(parcial):
    kwargs = _kwargs_de_conjunto_con_cuatrimestre(parcial)
    kwargs['numero_parcial'] = parcial.numero
    return kwargs


def kwargs_de_final(final):
    return {
        'fecha': final.fecha,
    }


def kwargs_de_conjunto(materiacarrera, conjunto):
    tipo_conjunto = conjuntos_utils.tipo_conjunto(conjunto)
    if tipo_conjunto == 'practica':
        kwargs = kwargs_de_practica(conjunto.practica)
    elif tipo_conjunto == 'parcial':
        kwargs = kwargs_de_parcial(conjunto.parcial)
    elif tipo_conjunto == 'final':
        kwargs = kwargs_de_final(conjunto.final)
    else:
        raise ValueError('Tipo de conjunto no conocido.')

    kwargs['materia_carrera'] = materiacarrera
    return kwargs


def namespace_de_conjunto(conjunto):
    tipo_conjunto = conjuntos_utils.tipo_conjunto(conjunto)
    if tipo_conjunto == 'practica':
        subdomain = 'practicas'
    elif tipo_conjunto == 'parcial':
        subdomain = \
            'recuperatorios' if conjunto.parcial.recuperatorio else 'parciales'
    elif tipo_conjunto == 'final':
        subdomain = 'finales'

    return 'materia:{}'.format(subdomain)


def nombre_url_conjunto(conjunto):
    namespace = namespace_de_conjunto(conjunto)
    tipo_conjunto = conjuntos_utils.tipo_conjunto(conjunto)
    return '{}:{}'.format(namespace, tipo_conjunto)


def url_conjunto(materiacarrera, conjunto):
    kwargs = kwargs_de_conjunto(materiacarrera, conjunto)
    nombre = nombre_url_conjunto(conjunto)
    return reverse(nombre, kwargs=kwargs)


def kwargs_a_conjunto(kwargs):
    tipo_conjunto = kwargs.get('conjunto')
    kwargs_objeto = {
        'materia': kwargs.get('materia_carrera').materia,
    }
    if tipo_conjunto == 'final':
        kwargs_objeto['fecha'] = kwargs.get('fecha')
        clase_conjunto = Final
    else:
        kwargs_objeto['anio'] = kwargs.get('anio')
        kwargs_objeto['cuatrimestre'] = kwargs.get('cuatrimestre')
        if tipo_conjunto == 'practica':
            clase_conjunto = Practica
            kwargs_objeto['numero'] = kwargs.get('numero_practica')
        elif tipo_conjunto == 'parcial':
            clase_conjunto = Parcial
            kwargs_objeto['numero'] = kwargs.get('numero_parcial')
            kwargs_objeto['recuperatorio'] = kwargs.get('recuperatorio')
        else:
            raise ValueError(
                'El parámetro conjunto no es ningún tipo conocido')

    return get_object_or_404(clase_conjunto, **kwargs_objeto)
