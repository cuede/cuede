from django.urls import reverse

from enunciados.utils import conjuntos_url_parser


def namespace_enunciado(enunciado):
    namespace_conjunto = conjuntos_url_parser.namespace_de_conjunto(
        enunciado.conjunto)
    return '{}:enunciados'.format(namespace_conjunto)


def kwargs_de_enunciado(materia_carrera, enunciado):
    kwargs = conjuntos_url_parser.kwargs_de_conjunto(
        materia_carrera, enunciado.conjunto)
    kwargs['numero'] = enunciado.numero
    return kwargs


def url_enunciado_con_nombre(materia_carrera, enunciado, nombre):
    namespace = namespace_enunciado(enunciado)
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
