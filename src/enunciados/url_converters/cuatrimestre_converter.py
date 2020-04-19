from django.urls.converters import StringConverter

from enunciados.utils import cuatrimestres_url_parser


class CuatrimestreConverter(StringConverter):
    def to_python(self, value):
        return cuatrimestres_url_parser.url_a_numero(value)

    def to_url(self, value):
        return cuatrimestres_url_parser.numero_a_url(value)