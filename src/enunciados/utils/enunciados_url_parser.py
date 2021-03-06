from django.shortcuts import get_object_or_404
from django.urls import reverse

from enunciados.utils import conjuntos_url_parser
from enunciados.models import Enunciado


def namespace_enunciado(conjunto):
    namespace_conjunto = conjuntos_url_parser.namespace_de_conjunto(conjunto)
    return '{}:enunciados'.format(namespace_conjunto)


def kwargs_de_enunciado(materia_carrera, enunciado):
    kwargs = conjuntos_url_parser.kwargs_de_conjunto(
        materia_carrera, enunciado.conjunto)
    kwargs['numero'] = enunciado.numero
    return kwargs


def url_enunciado_con_nombre(materia_carrera, enunciado, nombre):
    namespace = namespace_enunciado(enunciado.conjunto)
    nombre_url_enunciado = '{}:{}'.format(namespace, nombre)
    kwargs = kwargs_de_enunciado(materia_carrera, enunciado)
    return reverse(nombre_url_enunciado, kwargs=kwargs)


def url_enunciado(materia_carrera, enunciado):
    return url_enunciado_con_nombre(
        materia_carrera, enunciado, 'ver_enunciado')


def url_editar_enunciado(materia_carrera, enunciado):
    return url_enunciado_con_nombre(
        materia_carrera, enunciado, 'editar_enunciado')


def url_versiones_enunciado(materia_carrera, enunciado):
    return url_enunciado_con_nombre(
        materia_carrera, enunciado, 'versiones_enunciado')


def url_nuevo_enunciado(materia_carrera, conjunto):
    namespace = namespace_enunciado(conjunto)
    nombre_url = '{}:nuevo_enunciado'.format(namespace)
    kwargs = conjuntos_url_parser.kwargs_de_conjunto(materia_carrera, conjunto)
    return reverse(nombre_url, kwargs=kwargs)


def kwargs_a_enunciado(kwargs):
    conjunto = conjuntos_url_parser.kwargs_a_conjunto(kwargs)
    numero = kwargs.get('numero')
    return get_object_or_404(Enunciado, numero=numero, conjunto=conjunto)
