from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView

from enunciados.models import Final, Parcial, Practica
from enunciados.utils import conjuntos_url_parser, enunciados_url_parser
from enunciados.views.conjuntos_de_enunciados import conjuntos_de_enunciados_forms


def conjunto_de_enunciados(request, **kwargs):
    materia_carrera = kwargs['materia_carrera']
    conjunto = conjuntos_url_parser.kwargs_a_conjunto(kwargs)
    url_nuevo_enunciado = enunciados_url_parser.url_nuevo_enunciado(
        materia_carrera, conjunto)
    contexto = {
        'carrera': materia_carrera.carrera,
        'materia_carrera': materia_carrera,
        'conjunto': conjunto,
        'url_nuevo_enunciado': url_nuevo_enunciado,
    }
    return render(request, 'enunciados/conjunto_de_enunciados.html', contexto)


class CrearConjuntoDeEnunciadosView(CreateView):
    template_name = 'enunciados/nuevo_conjunto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.titulo
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['materia'] = self.kwargs['materia_carrera'].materia
        return kwargs

    def get_success_url(self):
        materia_carrera = self.kwargs['materia_carrera']
        return conjuntos_url_parser.url_conjunto(materia_carrera, self.object)


class CrearPracticaView(CrearConjuntoDeEnunciadosView):
    form_class = conjuntos_de_enunciados_forms.PracticaForm
    titulo = _('Nueva Práctica')


class CrearParcialView(CrearConjuntoDeEnunciadosView):
    form_class = conjuntos_de_enunciados_forms.ParcialForm
    titulo = _('Nuevo Parcial')


class CrearFinalView(CrearConjuntoDeEnunciadosView):
    form_class = conjuntos_de_enunciados_forms.FinalForm
    titulo = _('Nuevo Final')
