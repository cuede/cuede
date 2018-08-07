from django.views.generic.edit import CreateView
from django.forms import ModelForm
from django.shortcuts import redirect, render

from enunciados import cuatrimestres_url_parser
from enunciados.models import Enunciado, VersionTextoEnunciado
from . import enunciados_utils


def render_enunciado(request, enunciado_elegido):
    contexto = {'enunciado': enunciado_elegido}
    return render(request, 'enunciados/enunciado.html', contexto)


def enunciado_practica(request, materia, anio, cuatrimestre, numero_practica, numero):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = enunciados_utils.enunciado_de_practica(materia, anio, numero_cuatrimestre, numero_practica, numero)
    return render_enunciado(request, encontrado)


def enunciado_parcial(request, materia, anio, cuatrimestre, numero_parcial, numero, es_recuperatorio):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = enunciados_utils.enunciado_de_parcial(
        materia, anio, numero_cuatrimestre, numero_parcial, numero, es_recuperatorio)
    return render_enunciado(request, encontrado)


def enunciado_final(request, materia, anio, mes, dia, numero):
    encontrado = enunciados_utils.enunciado_de_final(materia, anio, mes, dia, numero)
    return render_enunciado(request, encontrado)


class VersionTextoForm(ModelForm):
    class Meta:
        fields = ['texto']
        model = VersionTextoEnunciado


class CrearEnunciado(CreateView):
    model = Enunciado
    fields = ['conjunto', 'numero']

    def get_context_data(self, **kwargs):
        context = super(CrearEnunciado, self).get_context_data(**kwargs)
        if self.request.POST:
            context['texto_form'] = VersionTextoForm(self.request.POST)
        else:
            context['texto_form'] = VersionTextoForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        texto_form = context['texto_form']
        if texto_form.is_valid() and form.is_valid():
            self.object = form.save()
            version_texto = texto_form.save(commit=False)
            version_texto.enunciado = self.object
            version_texto.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
