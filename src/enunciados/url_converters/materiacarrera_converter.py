import re

from django.urls.converters import SlugConverter

from enunciados.models import MateriaCarrera


class MateriaCarreraConverter:
    regex = '({carrera})/({materia})'.format(
        carrera=SlugConverter.regex, materia=SlugConverter.regex)

    def to_python(self, value):
        match = re.match(self.regex, value)
        slug_carrera = match.group(1)
        slug_materia = match.group(2)
        try:
            return MateriaCarrera.objects.get(
                slug=slug_materia, carrera__slug=slug_carrera)
        except MateriaCarrera.DoesNotExist:
            raise ValueError

    def to_url(self, value):
        return '{}/{}'.format(value.carrera.slug, value.slug)
