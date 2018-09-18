from django.urls import path, include

from enunciados.views import conjuntos_de_enunciados


app_name = 'parciales'

parcial_urlpatterns = [
    path('', conjuntos_de_enunciados.parcial, name='parcial'),
    path('', include('enunciados.urls.enunciados_urls',
                     namespace='enunciados_parcial')),
]

urlpatterns = [
    path('<int:anio>/<cuatrimestre>/<int:numero_parcial>/',
         include(parcial_urlpatterns)),
]
