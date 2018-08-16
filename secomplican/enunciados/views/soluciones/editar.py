from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect

from enunciados.models import Solucion, VersionTextoSolucion


class EditarSolucion(CreateView):
    model = VersionTextoSolucion
    fields = ['texto']
    template_name = 'enunciados/editar_solucion.html'

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.solucion = get_object_or_404(Solucion, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.solucion.enunciado.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.solucion = self.solucion
        self.object.save()
        return redirect(self.get_success_url())
