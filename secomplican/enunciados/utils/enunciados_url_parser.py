from django.urls import reverse

from enunciados.utils import conjuntos_url_parser


def namespace_enunciado(enunciado):
    namespace_conjunto = conjuntos_url_parser.namespace_de_conjunto(
        enunciado.conjunto)
    return '{}:enunciados'.format(namespace_conjunto)


def url_enunciado(materia_carrera, enunciado):
    namespace = namespace_enunciado(enunciado)
    nombre_url_enunciado = '{}:ver_enunciado'.format(namespace)
    kwargs = conjuntos_url_parser.kwargs_de_conjunto(
        materia_carrera, enunciado.conjunto)
    kwargs['numero'] = enunciado.numero
    return reverse(nombre_url_enunciado, kwargs=kwargs)
