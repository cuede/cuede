from django.urls.converters import SlugConverter

from enunciados.models import Materia


class MateriaConverter(SlugConverter):
    def to_python(self, value):
        try:
            return Materia.objects.get(slug=value)
        except Materia.DoesNotExist:
            raise ValueError

    def to_url(self, value):
        return value.slug