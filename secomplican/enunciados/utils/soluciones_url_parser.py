from django.urls import reverse

from enunciados.utils import enunciados_url_parser


def url_nueva_solucion(materia_carrera, enunciado):
    return enunciados_url_parser.url_enunciado_con_nombre(
        materia_carrera, enunciado, 'crear_solucion')


def kwargs_de_solucion(materia_carrera, solucion):
    return {
        'carrera': materia_carrera.carrera,
        'materia_carrera': materia_carrera,
        'pk': solucion.pk,
    }


def url_editar_solucion(materia_carrera, solucion):
    kwargs = kwargs_de_solucion(materia_carrera, solucion)
    return reverse('editar_solucion', kwargs=kwargs)
