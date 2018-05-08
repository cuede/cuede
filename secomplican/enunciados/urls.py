from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('materias', views.MateriasView.as_view(), name='materias'),
    path('<nombre>', views.materia, name='materia'),
    path('<materia>/<int:anio>/<cuatrimestre>/practicas/<int:numero>', views.practica, name='practica'),
    path('<materia>/<int:anio>/<cuatrimestre>/parciales/<int:numero>', views.parcial, name='parcial'),
    path('<materia>/<int:anio>/<cuatrimestre>/recuperatorios/<int:numero>', views.parcial, {'recuperatorio': True},
         name='recuperatorio'),
    path(
        '<materia>/<int:anio>/<cuatrimestre>/practicas/<int:conjunto_de_enunciados>/<int:numero>',
        views.enunciado,
        {'tipo_conjunto': 'practica'},
        name='enunciado_practica'
    ),
    path(
        '<materia>/<int:anio>/<cuatrimestre>/parciales/<int:conjunto_de_enunciados>/<int:numero>',
        views.enunciado,
        {'tipo_conjunto': 'parcial'},
        name='enunciado_parcial'
    ),
    path(
        '<materia>/<int:anio>/<cuatrimestre>/recuperatorios/<int:conjunto_de_enunciados>/<int:numero>',
        views.enunciado,
        {'tipo_conjunto': 'recuperatorio'},
        name='enunciado_recuperatorio'
    ),
]
