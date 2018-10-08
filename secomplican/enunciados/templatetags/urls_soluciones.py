from django import template

from enunciados.utils import soluciones_url_parser

register = template.Library()

register.simple_tag(soluciones_url_parser.url_editar_solucion)
register.simple_tag(soluciones_url_parser.url_versiones_solucion)
