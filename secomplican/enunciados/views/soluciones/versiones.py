from django.shortcuts import get_object_or_404

from enunciados.models import Solucion
from enunciados.views.versiones_view import VersionesView
from enunciados.utils import enunciados_url_parser


class VersionesSolucionView(VersionesView):
    template_name = 'enunciados/versiones_solucion.html'

    def get_object(self):
        pk = self.kwargs['pk_solucion']
        return get_object_or_404(Solucion, pk=pk)

    def get_success_url(self):
        materia_carrera = self.kwargs['materia_carrera']
        enunciado = self.get_object().enunciado
        return enunciados_url_parser.url_enunciado(materia_carrera, enunciado)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        materia_carrera = self.kwargs['materia_carrera']
        context['materia_carrera'] = materia_carrera
        context['carrera'] = materia_carrera.carrera
        context['solucion'] = self.get_object()
        return context
