from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('materias', views.MateriasView.as_view(), name='materias'),
    path('<nombre>', views.materia, name='materia'),
    path('<materia>/<int:anio>/<cuatrimestre>/practica<int:numero>', views.practica, name='practica'),
    path('<materia>/<int:anio>/<cuatrimestre>/practica<int:practica>/<int:numero>', views.enunciado, name='enunciado'),
]
