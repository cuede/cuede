from django.urls import reverse

from enunciados.utils import enunciados_url_parser


def url_nueva_solucion(materia_carrera, enunciado):
    return enunciados_url_parser.url_enunciado_con_nombre(
        materia_carrera, enunciado, 'crear_solucion')
