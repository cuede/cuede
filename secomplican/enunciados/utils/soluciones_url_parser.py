from django.urls import reverse

from enunciados.utils import conjuntos_url_parser, conjuntos_utils


def _nombre_url_nueva_solucion(enunciado):
    tipo_conjunto = conjuntos_utils.tipo_conjunto(enunciado.conjunto)
    if tipo_conjunto == 'practica':
        namespace = 'enunciados_practica'
    elif tipo_conjunto == 'parcial':
        if enunciado.parcial.recuperatorio:
            namespace = 'recuperatorios:enunciados_parcial'
        else:
            namespace = 'parciales:enunciados_parcial'
    elif tipo_conjunto == 'final':
        namespace = 'enunciados_final'

    return ':'.join(['materia', namespace, 'crear_solucion'])


def url_nueva_solucion(materia_carrera, enunciado):
    nombre_url = _nombre_url_nueva_solucion(enunciado)

    tipo_conjunto = conjuntos_utils.tipo_conjunto(enunciado.conjunto)
    kwargs = {}
    if tipo_conjunto == 'practica':
        kwargs = conjuntos_url_parser.kwargs_de_practica(
            enunciado.conjunto.practica)
    elif tipo_conjunto == 'parcial':
        kwargs = conjuntos_url_parser.kwargs_de_parcial(
            enunciado.conjunto.parcial)
    elif tipo_conjunto == 'final':
        kwargs = conjuntos_url_parser.kwargs_de_final(
            enunciado.conjunto.final)

    kwargs['materia_carrera'] = materia_carrera
    kwargs['numero'] = enunciado.numero
    return reverse(nombre_url, kwargs=kwargs)
