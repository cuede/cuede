from django.urls import reverse

from enunciados.utils import enunciados_url_parser


def url_nueva_solucion(materia_carrera, enunciado):
    return enunciados_url_parser.url_enunciado_con_nombre(
        materia_carrera, enunciado, 'crear_solucion')


def kwargs_de_solucion(materia_carrera, solucion):
    kwargs = enunciados_url_parser.kwargs_de_enunciado(
        materia_carrera, solucion.enunciado_padre)
    kwargs['pk_solucion'] = solucion.pk
    return kwargs


def url_solucion_con_nombre(materia_carrera, nombre, solucion):
    namespace = enunciados_url_parser.namespace_enunciado(
        solucion.enunciado_padre.conjunto)
    nombre_url = '{}:{}'.format(namespace, nombre)
    kwargs = kwargs_de_solucion(materia_carrera, solucion)
    return reverse(nombre_url, kwargs=kwargs)


def url_editar_solucion(materia_carrera, solucion):
    return url_solucion_con_nombre(
        materia_carrera, 'editar_solucion', solucion)


def url_versiones_solucion(materia_carrera, solucion):
    return url_solucion_con_nombre(
        materia_carrera, 'versiones_solucion', solucion)
