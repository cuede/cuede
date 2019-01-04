from django.shortcuts import render, redirect, get_object_or_404

from enunciados.models import Enunciado
from enunciados.utils import cuatrimestres_url_parser, enunciados_url_parser
from enunciados.views.versiones_view import VersionesView
from enunciados.views.breadcrumb import breadcrumb_versiones_enunciado


class VersionesEnunciadoView(VersionesView):
    template_name = 'enunciados/versiones_enunciado.html'

    def get_object(self):
        return enunciados_url_parser.kwargs_a_enunciado(self.kwargs)

    def get_success_url(self):
        materia_carrera = self.kwargs['materia_carrera']
        return enunciados_url_parser.url_enunciado(
            materia_carrera, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        materia_carrera = self.kwargs['materia_carrera']
        context['materia_carrera'] = materia_carrera
        context['carrera'] = materia_carrera.carrera
        context['enunciado'] = self.get_object()
        context['breadcrumb'] = breadcrumb_versiones_enunciado(
            materia_carrera, self.get_object())
        return context
