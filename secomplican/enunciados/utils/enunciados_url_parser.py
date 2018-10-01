from django.urls import reverse

from enunciados.utils import conjuntos_url_parser


def url_enunciado(materia_carrera, enunciado):
    nombre_url_conjunto = conjuntos_url_parser.nombre_url_conjunto(
        materia_carrera, enunciado.conjunto)
    nombre_url_enunciado = '{}:ver_enunciado'.format(nombre_url_conjunto)
    kwargs = conjuntos_url_parser.kwargs_de_conjunto(
        materia_carrera, enunciado.conjunto)
    kwargs['numero'] = enunciado.numero
    return reverse(nombre_url_enunciado, kwargs=kwargs)
