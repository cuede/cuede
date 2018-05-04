from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('materias', views.MateriasView.as_view(), name='materias'),
    path('<nombre>', views.materia, name='materia'),
    path('<materia>/<int:anio>/<cuatrimestre>/practicas/<int:numero>', views.practica, name='practica'),
    path('<materia>/<int:anio>/<cuatrimestre>/parciales/<int:numero>', views.parcial, name='parcial'),
    path('<materia>/<int:anio>/<cuatrimestre>/practicas/<int:practica>/<int:numero>', views.enunciado,
         name='enunciado'),
]
