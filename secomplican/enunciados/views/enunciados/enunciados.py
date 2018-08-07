from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.forms import ModelForm
from django.shortcuts import redirect, render

from enunciados import cuatrimestres_url_parser
from enunciados.models import Enunciado, VersionTextoEnunciado


def render_enunciado(request, enunciado_elegido):
    contexto = {'enunciado': enunciado_elegido}
    return render(request, 'enunciados/enunciado.html', contexto)


def enunciado_practica(request, materia, anio, cuatrimestre, numero_practica, numero):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = get_object_or_404(
        Enunciado,
        conjunto__materia__nombre=materia,
        numero=numero,
        conjunto__practica__isnull=False,
        conjunto__practica__cuatrimestre__anio=anio,
        conjunto__practica__cuatrimestre__numero=numero_cuatrimestre,
        conjunto__practica__numero=numero_practica,
    )
    return render_enunciado(request, encontrado)


def enunciado_parcial(request, materia, anio, cuatrimestre, numero_parcial, numero, es_recuperatorio):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = get_object_or_404(
        Enunciado,
        conjunto__materia__nombre=materia,
        numero=numero,
        conjunto__parcial__isnull=False,
        conjunto__parcial__cuatrimestre__anio=anio,
        conjunto__parcial__cuatrimestre__numero=numero_cuatrimestre,
        conjunto__parcial__numero=numero_parcial,
        conjunto__parcial__recuperatorio=es_recuperatorio,
    )
    return render_enunciado(request, encontrado)


def enunciado_final(request, materia, anio, mes, dia, numero):
    encontrado = get_object_or_404(
        Enunciado,
        conjunto__materia__nombre=materia,
        numero=numero,
        conjunto__final__isnull=False,
        conjunto__final__fecha__year=anio,
        conjunto__final__fecha__month=mes,
        conjunto__final__fecha__day=dia,
    )

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
