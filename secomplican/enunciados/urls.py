from django.urls import path

from enunciados.views import index, materias, conjuntos_de_enunciados
from enunciados.views.enunciados import enunciados
from enunciados.views.enunciados import crear
from enunciados.views.enunciados import soluciones


urlpatterns = [
    path('', index.index, name='index'),
    path('materias/', materias.MateriasView.as_view(), name='materias'),
    path('<slug:nombre>/', materias.materia, name='materia'),
    path('<slug:materia>/practicas/<int:anio>/<cuatrimestre>/<int:numero>/',
         conjuntos_de_enunciados.practica, name='practica'),
    path('<slug:materia>/parciales/<int:anio>/<cuatrimestre>/<int:numero>/',
         conjuntos_de_enunciados.parcial, name='parcial'),
    path('<slug:materia>/recuperatorios/<int:anio>/<cuatrimestre>/<int:numero>/',
         conjuntos_de_enunciados.parcial, {'recuperatorio': True},
         name='recuperatorio'),
    path('<slug:materia>/finales/<int:anio>/<int:mes>/<int:dia>/',
         conjuntos_de_enunciados.final, name='final'),

    # Enunciados
    path(
        '<slug:materia>/practicas/<int:anio>/<cuatrimestre>/<int:numero_practica>/<int:numero>/',
        enunciados.enunciado_practica,
        name='enunciado_practica'
    ),
    path(
        '<slug:materia>/parciales/<int:anio>/<cuatrimestre>/<int:numero_parcial>/<int:numero>/',
        enunciados.enunciado_parcial,
        {'es_recuperatorio': False},
        name='enunciado_parcial'
    ),
    path(
        '<slug:materia>/recuperatorios/<int:anio>/<cuatrimestre>/<int:numero_parcial>/<int:numero>/',
        enunciados.enunciado_parcial,
        {'es_recuperatorio': True},
        name='enunciado_recuperatorio'
    ),
    path(
        '<slug:materia>/finales/<int:anio>/<int:mes>/<int:dia>/<int:numero>/',
        enunciados.enunciado_final,
        name='enunciado_final'
    ),

    # Soluciones
    path(
        '<slug:materia>/practicas/<int:anio>/<cuatrimestre>/<int:numero_practica>/<int:numero>/nuevaSolucion/',
        soluciones.CrearSolucion.as_view(),
        name='solucion_practica'
    ),
    path(
        '<slug:materia>/parciales/<int:anio>/<cuatrimestre>/<int:numero_parcial>/<int:numero>/nuevaSolucion/',
        soluciones.CrearSolucion.as_view(),
        {'es_recuperatorio': False},
        name='solucion_parcial'
    ),
    path(
        '<slug:materia>/recuperatorios/<int:anio>/<cuatrimestre>/<int:numero_parcial>/<int:numero>/nuevaSolucion/',
        soluciones.CrearSolucion.as_view(),
        {'es_recuperatorio': True},
        name='solucion_recuperatorio'
    ),
    path(
        '<slug:materia>/finales/<int:anio>/<int:mes>/<int:dia>/<int:numero>/nuevaSolucion/',
        soluciones.CrearSolucion.as_view(),
        name='solucion_final'
    ),

    path(
        '<slug:materia>/nuevo-enunciado/',
        crear.nuevo_enunciado,
        name='agregar_enunciado'
    ),
]
