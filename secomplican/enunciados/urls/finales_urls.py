from django.urls import path, include, register_converter

from enunciados.views import conjuntos_de_enunciados
from enunciados.url_converters import FechaConverter

register_converter(FechaConverter, 'fecha')

final_urlpatterns = [
    path('', conjuntos_de_enunciados.final, name='final'),
    path('',
         include('enunciados.urls.enunciados_urls',
                 namespace='enunciados_final'),
         kwargs={'conjunto': 'final'}),
]

urlpatterns = [
    path('<fecha:fecha>/', include(final_urlpatterns)),
]