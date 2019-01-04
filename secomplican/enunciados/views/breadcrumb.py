from django.urls import reverse

from enunciados.utils import conjuntos_utils
from enunciados.utils import conjuntos_url_parser
from enunciados.utils import enunciados_url_parser


class BreadcrumbPage:
    def __init__(self, title, url=None):
        self.title = title
        self.url = url


def breadcrumb_materia(materia_carrera):
    return [
        BreadcrumbPage(
            materia_carrera.carrera,
            reverse('materias', kwargs={
                'carrera': materia_carrera.carrera})
        ),
        BreadcrumbPage(materia_carrera, materia_carrera.get_absolute_url()),
    ]


def breadcrumb_practicas(materia_carrera):
    return breadcrumb_materia(materia_carrera) + [
        BreadcrumbPage("Prácticas")
    ]


def breadcrumb_conjunto_de_enunciados(materia_carrera, conjunto):
    return breadcrumb_materia(materia_carrera) + [
        BreadcrumbPage(
            conjunto,
            conjuntos_url_parser.url_conjunto(materia_carrera, conjunto)
        )
    ]


def breadcrumb_ver_enunciado(materia_carrera, enunciado):
    breadcrumb_conjunto = breadcrumb_conjunto_de_enunciados(
        materia_carrera, conjuntos_utils.castear_a_subclase(enunciado.conjunto)
    )
    return breadcrumb_conjunto + [
        BreadcrumbPage(
            enunciado,
            enunciados_url_parser.url_enunciado(materia_carrera, enunciado)
        )
    ]


def breadcrumb_crear_enunciado(materia_carrera, conjunto):
    return breadcrumb_conjunto_de_enunciados(materia_carrera, conjunto) + [
        BreadcrumbPage("Nuevo ejercicio")
    ]


def breadcrumb_editar_enunciado(materia_carrera, enunciado):
    return breadcrumb_ver_enunciado(materia_carrera, enunciado) + [
        BreadcrumbPage("Editar ejercicio")
    ]


def breadcrumb_versiones_enunciado(materia_carrera, enunciado):
    return breadcrumb_ver_enunciado(materia_carrera, enunciado) + [
        BreadcrumbPage("Versiones anteriores")
    ]


def breadcrumb_editar_solucion(materia_carrera, enunciado):
    return breadcrumb_ver_enunciado(materia_carrera, enunciado) + [
        BreadcrumbPage("Editar solución")
    ]
