import re

from django.urls.converters import SlugConverter

from enunciados.models import Carrera


class CarreraConverter(SlugConverter):
    def to_python(self, value):
        try:
            return Carrera.objects.get(slug=value)
        except Carrera.DoesNotExist:
            raise ValueError

    def to_url(self, value):
        return value.slug
