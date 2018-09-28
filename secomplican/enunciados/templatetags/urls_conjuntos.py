from django import template

from enunciados.utils import conjuntos_url_parser

register = template.Library()

register.simple_tag(conjuntos_url_parser.url_practica)
register.simple_tag(conjuntos_url_parser.url_parcial)
register.simple_tag(conjuntos_url_parser.url_final)
