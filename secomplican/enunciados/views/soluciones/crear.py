from django.shortcuts import redirect
from django.utils.translation import gettext
from django.views.generic.edit import CreateView
from enunciados.models import Solucion, VersionTextoSolucion
from enunciados.utils import cuatrimestres_url_parser, enunciados_url_parser
from enunciados.views.breadcrumb import breadcrumb_crear_solucion


class CrearSolucion(CreateView):
    model = VersionTextoSolucion
    fields = ['texto']
    template_name = 'enunciados/nueva_solucion.html'

    def dispatch(self, request, *args, **kwargs):
        self.enunciado = enunciados_url_parser.kwargs_a_enunciado(self.kwargs)
        self.materia_carrera = kwargs['materia_carrera']
        return super(CrearSolucion, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return enunciados_url_parser.url_enunciado(
            self.materia_carrera, self.enunciado)

    def get_context_data(self, **kwargs):
        context = super(CrearSolucion, self).get_context_data(**kwargs)
        context['enunciado'] = self.enunciado
        context['materia_carrera'] = self.materia_carrera
        context['carrera'] = self.materia_carrera.carrera
        context['breadcrumb'] = breadcrumb_crear_solucion(
            self.materia_carrera, self.enunciado)
        context['texto_boton'] = gettext('Crear')
        return context

    def form_valid(self, form):
        solucion = Solucion(enunciado=self.enunciado)
        solucion.enunciado = self.enunciado
        solucion.save()
        self.object = form.save(commit=False)
        self.object.solucion = solucion
        self.object.save()
        return redirect(self.get_success_url())
