from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('materias', views.materias, name='materias')
]
