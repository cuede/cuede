from django.urls import path, include, register_converter

from enunciados.views import conjuntos_de_enunciados
from enunciados.url_converters import CuatrimestreConverter

register_converter(CuatrimestreConverter, 'cuatrimestre')

app_name = 'parciales'

parcial_urlpatterns = [
    path('', conjuntos_de_enunciados.parcial, name='parcial'),
    path('',
         include('enunciados.urls.enunciados_urls',
                 namespace='enunciados_parcial'),
         kwargs={'conjunto': 'parcial'}),
]

urlpatterns = [
    path('<int:anio>/<cuatrimestre:cuatrimestre>/<int:numero_parcial>/',
         include(parcial_urlpatterns)),
]
