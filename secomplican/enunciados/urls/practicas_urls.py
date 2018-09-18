from django.urls import path, include

from enunciados.views import practicas, conjuntos_de_enunciados


practica_urlpatterns = [
    path('', conjuntos_de_enunciados.practica, name='practica'),
    path('', include('enunciados.urls.enunciados_urls',
                     namespace='enunciados_practica')),
]

urlpatterns = [
    path('', practicas.practicas, name='practicas'),
    path('<int:anio>/<cuatrimestre>/<int:numero_practica>/',
         include(practica_urlpatterns)),
]
