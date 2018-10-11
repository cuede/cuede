from django.urls import path, include, register_converter

from enunciados.views.conjuntos_de_enunciados import conjuntos_de_enunciados
from enunciados.url_converters import FechaConverter

register_converter(FechaConverter, 'fecha')

app_name = 'finales'

final_urlpatterns = [
    path('', conjuntos_de_enunciados.conjunto_de_enunciados, name='final'),
    path(
        '',
        include('enunciados.urls.enunciados_urls', namespace='enunciados'),
    ),
]

urlpatterns = [
    path(
        '<fecha:fecha>/',
        include((final_urlpatterns, 'final')),
        kwargs={'conjunto': 'final'}
    ),
]
