from django.shortcuts import get_object_or_404

from enunciados.models import Solucion
from enunciados.views.versiones_view import VersionesView


class VersionesSolucionView(VersionesView):
    template_name = 'enunciados/versiones_solucion.html'

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Solucion, pk=pk)

    def get_success_url(self):
        return self.get_object().enunciado.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solucion'] = self.get_object()
        return context
