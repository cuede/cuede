from django import template

from enunciados.utils import cuatrimestres_parser

register = template.Library()

@register.filter
def texto_cuatrimestre(numero):
    """Devuelve un texto correspondiente al número de este cuatrimestre"""
    return cuatrimestres_parser.numero_a_texto(numero)