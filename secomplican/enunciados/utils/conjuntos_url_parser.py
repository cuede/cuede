from django.urls import reverse

from enunciados.utils import cuatrimestres_url_parser


def url_conjunto(materiacarrera, nombre, kwargs):
    kwargs['materia_carrera'] = materiacarrera
    nombre = 'materia:{}'.format(nombre)
    return reverse(nombre, kwargs=kwargs)


def url_conjunto_con_cuatrimestre(materiacarrera, nombre, kwargs, conjunto):
    kwargs['anio'] = conjunto.anio
    kwargs['cuatrimestre'] = conjunto.cuatrimestre
    return url_conjunto(materiacarrera, nombre, kwargs)


def url_practica(materiacarrera, practica):
    kwargs = {
        'numero_practica': practica.numero,
    }
    return url_conjunto_con_cuatrimestre(
        materiacarrera, 'practica', kwargs, practica)
