from django.urls import path

from enunciados.views import index, materias, conjuntos_de_enunciados, enunciados

urlpatterns = [
    path('', index.index, name='index'),
    path('materias', materias.MateriasView.as_view(), name='materias'),
    path('<nombre>', materias.materia, name='materia'),
    path('<materia>/<int:anio>/<cuatrimestre>/practicas/<int:numero>',
         conjuntos_de_enunciados.practica, name='practica'),
    path('<materia>/<int:anio>/<cuatrimestre>/parciales/<int:numero>', conjuntos_de_enunciados.parcial, name='parcial'),
    path('<materia>/<int:anio>/<cuatrimestre>/recuperatorios/<int:numero>',
         conjuntos_de_enunciados.parcial, {'recuperatorio': True},
         name='recuperatorio'),
    path('<materia>/finales/<int:anio>/<int:mes>/<int:dia>', conjuntos_de_enunciados.final, name='final'),
    path(
        '<materia>/<int:anio>/<cuatrimestre>/practicas/<int:conjunto_de_enunciados>/<int:numero>',
        enunciados.enunciado,
        {'tipo_conjunto': 'practica'},
        name='enunciado_practica'
    ),
    path(
        '<materia>/<int:anio>/<cuatrimestre>/parciales/<int:conjunto_de_enunciados>/<int:numero>',
        enunciados.enunciado,
        {'tipo_conjunto': 'parcial'},
        name='enunciado_parcial'
    ),
    path(
        '<materia>/<int:anio>/<cuatrimestre>/recuperatorios/<int:conjunto_de_enunciados>/<int:numero>',
        enunciados.enunciado,
        {'tipo_conjunto': 'recuperatorio'},
        name='enunciado_recuperatorio'
    ),
    path(
        '<materia>/finales/<int:anio>/<int:mes>/<int:dia>/<int:numero>',
        enunciados.enunciado_final,
        name='enunciado_final'
    ),
    path(
        '<materia>/agregarEnunciado',
        enunciados.CrearEnunciado.as_view(),
        name='agregar_enunciado'
    )
]
