from django.urls import path, include, register_converter

from enunciados.views import practicas, conjuntos_de_enunciados

from enunciados.url_converters import CuatrimestreConverter

register_converter(CuatrimestreConverter, 'cuatrimestre')

practica_urlpatterns = [
    path('', conjuntos_de_enunciados.practica, name='practica'),
    path('',
         include('enunciados.urls.enunciados_urls',
                 namespace='enunciados_practica'),
         kwargs={'conjunto': 'practica'}),
]

urlpatterns = [
    path('', practicas.practicas, name='practicas'),
    path('<int:anio>/<cuatrimestre:cuatrimestre>/<int:numero_practica>/',
         include(practica_urlpatterns)),
]
