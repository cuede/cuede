from django.urls import path

from enunciados.views import index, materias, conjuntos_de_enunciados
from enunciados.views.enunciados import enunciados
from enunciados.views.enunciados import crear
from enunciados.views.enunciados import soluciones


urlpatterns = [
    path('', index.index, name='index'),
    path('materias/', materias.MateriasView.as_view(), name='materias'),
    path('<slug:nombre>/', materias.materia, name='materia'),
    path('<materia>/practicas/<int:anio>/<cuatrimestre>/<int:numero>/',
         conjuntos_de_enunciados.practica, name='practica'),
    path('<materia>/parciales/<int:anio>/<cuatrimestre>/<int:numero>/', conjuntos_de_enunciados.parcial, name='parcial'),
    path('<materia>/recuperatorios/<int:anio>/<cuatrimestre>/<int:numero>/',
         conjuntos_de_enunciados.parcial, {'recuperatorio': True},
         name='recuperatorio'),
    path('<materia>/finales/<int:anio>/<int:mes>/<int:dia>/', conjuntos_de_enunciados.final, name='final'),

    # Enunciados
    path(
        '<materia>/practicas/<int:anio>/<cuatrimestre>/<int:numero_practica>/<int:numero>/',
        enunciados.enunciado_practica,
        name='enunciado_practica'
    ),
    path(
        '<materia>/parciales/<int:anio>/<cuatrimestre>/<int:numero_parcial>/<int:numero>/',
        enunciados.enunciado_parcial,
        {'es_recuperatorio': False},
        name='enunciado_parcial'
    ),
    path(
        '<materia>/recuperatorios/<int:anio>/<cuatrimestre>/<int:numero_parcial>/<int:numero>/',
        enunciados.enunciado_parcial,
        {'es_recuperatorio': True},
        name='enunciado_recuperatorio'
    ),
    path(
        '<materia>/finales/<int:anio>/<int:mes>/<int:dia>/<int:numero>/',
        enunciados.enunciado_final,
        name='enunciado_final'
    ),

    # Soluciones
    path(
        '<materia>/practicas/<int:anio>/<cuatrimestre>/<int:numero_practica>/<int:numero>/nuevaSolucion/',
        soluciones.CrearSolucion.as_view(),
        name='solucion_practica'
    ),
    path(
        '<materia>/parciales/<int:anio>/<cuatrimestre>/<int:numero_parcial>/<int:numero>/nuevaSolucion/',
        soluciones.CrearSolucion.as_view(),
        {'es_recuperatorio': False},
        name='solucion_parcial'
    ),
    path(
        '<materia>/recuperatorios/<int:anio>/<cuatrimestre>/<int:numero_parcial>/<int:numero>/nuevaSolucion/',
        soluciones.CrearSolucion.as_view(),
        {'es_recuperatorio': True},
        name='solucion_recuperatorio'
    ),
    path(
        '<materia>/finales/<int:anio>/<int:mes>/<int:dia>/<int:numero>/nuevaSolucion/',
        soluciones.CrearSolucion.as_view(),
        name='solucion_final'
    ),

    path(
        '<materia>/nuevoEnunciado/',
        crear.nuevo_enunciado,
        name='agregar_enunciado'
    ),
]
