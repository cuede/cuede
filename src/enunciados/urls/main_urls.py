from django.urls import include, path, register_converter

from enunciados.url_converters import CarreraConverter, MateriaCarreraConverter
from enunciados.views import index, materias, que_es_esta_pagina
from enunciados.views.format_post import format_post

register_converter(CarreraConverter, 'carrera')
register_converter(MateriaCarreraConverter, 'materiacarrera')

urlpatterns = [
    path('que_es_esta_pagina', que_es_esta_pagina.que_es_esta_pagina, name='que_es_esta_pagina'),
    path('', index.index, name='index'),
    path(
        '<carrera:carrera>/materias/',
        materias.MateriasView.as_view(),
        name='materias'
    ),
    path(
        '<materiacarrera:materia_carrera>/',
        include('enunciados.urls.materia_urls', namespace='materia')
    ),
    path(
        'soluciones/<int:id_solucion>/',
        include('enunciados.urls.soluciones_urls', namespace='solucion')
    ),
    path('ajax/format_post/', format_post, name='format-post'),
]
