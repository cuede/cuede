from django.urls import path, include, register_converter

from enunciados.views.conjuntos_de_enunciados import conjuntos_de_enunciados
from enunciados.url_converters import CuatrimestreConverter

register_converter(CuatrimestreConverter, 'cuatrimestre')

app_name = 'parciales'

parcial_urlpatterns = [
    path('', conjuntos_de_enunciados.conjunto_de_enunciados, name='parcial'),
    path(
        '',
        include('enunciados.urls.enunciados_urls', namespace='enunciados'),
    ),
]

urlpatterns = [
    path(
        '<int:anio>/<cuatrimestre:cuatrimestre>/<int:numero_parcial>/',
        include((parcial_urlpatterns, 'parcial')),
        kwargs={'conjunto': 'parcial'},
    ),
]
