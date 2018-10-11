from django.urls import path, include

from enunciados.views import materias, conjuntos_de_enunciados

app_name = 'materia'

urlpatterns = [
    path('', materias.materia, name='materia'),
    path(
        'practicas/',
        include('enunciados.urls.practicas_urls', namespace='practicas')
    ),
    path(
        'parciales/',
        include('enunciados.urls.parciales_urls', namespace='parciales'),
        kwargs={'recuperatorio': False},
    ),
    path(
        'recuperatorios/',
        include('enunciados.urls.parciales_urls', namespace='recuperatorios'),
        kwargs={'recuperatorio': True},
    ),
    path(
        'finales/',
        include('enunciados.urls.finales_urls', namespace='finales')
    ),
    path(
        'agregar-practica/',
        conjuntos_de_enunciados.CrearPracticaView.as_view(),
        name='crear_practica',
    ),
    path(
        'agregar-parcial/',
        conjuntos_de_enunciados.CrearParcialView.as_view(),
        name='crear_parcial',
    ),
    path(
        'agregar-final/',
        conjuntos_de_enunciados.CrearFinalView.as_view(),
        name='crear_final',
    ),
]
