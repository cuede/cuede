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


def nombre_url_conjunto(materiacarrera, conjunto):
    tipo_conjunto = conjuntos_utils.tipo_conjunto(conjunto)
    nombre = tipo_conjunto
    if tipo_conjunto == 'parcial':
        subdomain = \
            'recuperatorios' if conjunto.parcial.recuperatorio else 'parciales'
        nombre = '{}:{}'.format(subdomain, nombre)
    return 'materia:{}'.format(nombre)


def url_conjunto(materiacarrera, conjunto, kwargs):
    kwargs['materia_carrera'] = materiacarrera
    nombre = nombre_url_conjunto(materiacarrera, conjunto)
    return reverse(nombre, kwargs=kwargs)


def url_practica(materiacarrera, practica):
    kwargs = kwargs_de_practica(practica)
    return url_conjunto(materiacarrera, practica, kwargs)


def url_parcial(materiacarrera, parcial):
    kwargs = kwargs_de_parcial(parcial)
    return url_conjunto(materiacarrera, parcial, kwargs)


def url_final(materiacarrera, final):
    return url_conjunto(materiacarrera, final, kwargs_de_final(final))


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
