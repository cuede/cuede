from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from enunciados.utils import cuatrimestres_url_parser
from enunciados.models import Solucion, VersionTextoSolucion
from . import enunciados_utils


def enunciado_con_kwargs(kwargs):
    if 'numero_parcial' in kwargs:
        numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(kwargs['cuatrimestre'])
        return enunciados_utils.enunciado_de_parcial(
            kwargs['materia'], kwargs['anio'], numero_cuatrimestre,
            kwargs['numero_parcial'], kwargs['numero'], kwargs['es_recuperatorio'])
    elif 'numero_practica' in kwargs:
        numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(kwargs['cuatrimestre'])
        return enunciados_utils.enunciado_de_practica(
            kwargs['materia'], kwargs['anio'], numero_cuatrimestre,
            kwargs['numero_practica'], kwargs['numero'])
    else:
        return enunciados_utils.enunciado_de_final(
            kwargs['materia'], kwargs['anio'], kwargs['mes'], kwargs['dia'], kwargs['numero'])


class CrearSolucion(CreateView):
    model = VersionTextoSolucion
    fields = ['texto']
    template_name = 'enunciados/nueva_solucion.html'

    def dispatch(self, request, *args, **kwargs):
        self.enunciado = enunciado_con_kwargs(self.kwargs)
        return super(CrearSolucion, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.enunciado.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(CrearSolucion, self).get_context_data(**kwargs)
        context['enunciado'] = self.enunciado
        return context

    def form_valid(self, form):
        if form.is_valid():
            solucion = Solucion(enunciado=self.enunciado)
            solucion.enunciado = self.enunciado
            solucion.save()
            self.object = form.save(commit=False)
            self.object.solucion = solucion
            self.object.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
