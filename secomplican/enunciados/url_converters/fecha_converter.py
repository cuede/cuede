from django.urls.converters import StringConverter
from datetime import date
import re


class FechaConverter:
    regex_anio = r'\d{4}'
    regex_mes = r'\d{1,2}'
    regex_dia = r'\d{1,2}'
    regex = '({})/({})/({})'.format(regex_anio, regex_mes, regex_dia)

    def to_python(self, value):
        match = re.match(self.regex, value)
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        return date(year, month, day)

    def to_url(self, value):
        return '{}/{}/{}'.format(value.year, value.month, value.day)
