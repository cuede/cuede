from django.utils.translation import gettext as _
from django.views.generic import CreateView
from enunciados.utils import conjuntos_url_parser
from enunciados.views.breadcrumb import breadcrumb_crear_conjunto_de_enunciados
from enunciados.views.conjuntos_de_enunciados import conjuntos_de_enunciados_forms


class CrearConjuntoDeEnunciadosView(CreateView):
    template_name = 'enunciados/nuevo_conjunto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        materia_carrera = self.kwargs['materia_carrera']
        context['titulo'] = self.titulo
        context['carrera'] = materia_carrera.carrera
        context['materia_carrera'] = materia_carrera
        context['breadcrumb'] = breadcrumb_crear_conjunto_de_enunciados(
            materia_carrera, self.titulo)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['materia_carrera'] = self.kwargs['materia_carrera']
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
