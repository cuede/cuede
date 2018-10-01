from django.urls import reverse

from enunciados.utils import conjuntos_url_parser


def url_enunciado(materia_carrera, enunciado):
    namespace_conjunto = conjuntos_url_parser.namespace_de_conjunto(
        enunciado.conjunto)
    nombre_url_enunciado = '{}:enunciados:ver_enunciado'.format(
        namespace_conjunto)
    kwargs = conjuntos_url_parser.kwargs_de_conjunto(
        materia_carrera, enunciado.conjunto)
    kwargs['numero'] = enunciado.numero
    return reverse(nombre_url_enunciado, kwargs=kwargs)
