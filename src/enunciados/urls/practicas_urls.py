from django.urls import path, include, register_converter

from enunciados.views import practicas
from enunciados.views.conjuntos_de_enunciados import conjuntos_de_enunciados
from enunciados.url_converters import CuatrimestreConverter

register_converter(CuatrimestreConverter, 'cuatrimestre')

app_name = 'practicas'

practica_urlpatterns = [
    path('', conjuntos_de_enunciados.conjunto_de_enunciados, name='practica'),
    path(
        '',
        include('enunciados.urls.enunciados_urls', namespace='enunciados'),
    ),
]

urlpatterns = [
    path('', practicas.practicas, name='practicas'),
    path(
        '<int:anio>/<cuatrimestre:cuatrimestre>/<int:numero_practica>/',
        include((practica_urlpatterns, 'practica')),
        kwargs={'conjunto': 'practica'},
    ),
]
