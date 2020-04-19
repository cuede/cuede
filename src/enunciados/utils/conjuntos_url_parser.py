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
    conjunto_casteado = conjuntos_utils.castear_a_subclase(conjunto)
    if isinstance(conjunto_casteado, Practica):
        kwargs = kwargs_de_practica(conjunto_casteado)
    elif isinstance(conjunto_casteado, Parcial):
        kwargs = kwargs_de_parcial(conjunto_casteado)
    elif isinstance(conjunto_casteado, Final):
        kwargs = kwargs_de_final(conjunto_casteado)
    else:
        raise ValueError('Tipo de conjunto no conocido.')

    kwargs['materia_carrera'] = materiacarrera
    return kwargs


def _subnamespace_url_conjunto(conjunto):
    conjunto_casteado = conjuntos_utils.castear_a_subclase(conjunto)
    if isinstance(conjunto_casteado, Practica):
        return 'practica'
    elif isinstance(conjunto_casteado, Parcial):
        return 'parcial'
    elif isinstance(conjunto_casteado, Final):
        return 'final'


def namespace_de_conjunto(conjunto):
    conjunto_casteado = conjuntos_utils.castear_a_subclase(conjunto)
    if isinstance(conjunto_casteado, Practica):
        subdomain = 'practicas'
    elif isinstance(conjunto_casteado, Parcial):
        subdomain = \
            'recuperatorios' if conjunto_casteado.recuperatorio else 'parciales'
    elif isinstance(conjunto_casteado, Final):
        subdomain = 'finales'
    namespace = _subnamespace_url_conjunto(conjunto)
    return 'materia:{}:{}'.format(subdomain, namespace)


def nombre_url_conjunto(conjunto):
    namespace = namespace_de_conjunto(conjunto)
    subnamespace = _subnamespace_url_conjunto(conjunto)
    return '{}:{}'.format(namespace, subnamespace)


def url_conjunto(materiacarrera, conjunto):
    """Devuelve la URL para poder ver el conjunto."""
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
