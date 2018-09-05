from django.shortcuts import render, redirect, get_object_or_404

from enunciados.models import Enunciado
from enunciados.utils import cuatrimestres_url_parser
from . import enunciados_utils
from enunciados.views.versiones_view import VersionesView


class VersionesEnunciadoView(VersionesView):
    template_name = 'enunciados/versiones_enunciado.html'

    def get_object(self):
        return enunciados_utils.enunciado_con_kwargs(self.kwargs)

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enunciado'] = self.get_object()
        return context
