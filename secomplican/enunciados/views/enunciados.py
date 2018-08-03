from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.forms import ModelForm
from django.shortcuts import redirect

from enunciados import cuatrimestres_url_parser
from enunciados.models import Enunciado, VersionTextoEnunciado


def render_enunciado(enunciado_elegido):
    return HttpResponse('{}'.format(enunciado_elegido.versiones.ultima()))


def enunciado(request, materia, anio, cuatrimestre, conjunto_de_enunciados, tipo_conjunto, numero):
    encontrados = Enunciado.objects.filter(
        conjunto__materia__nombre=materia,
        conjunto__cuatrimestre__anio=anio,
        conjunto__cuatrimestre__numero=cuatrimestres_url_parser.url_a_numero(cuatrimestre),
        numero=numero,
    )
    if tipo_conjunto == 'practica':
        encontrados = encontrados.filter(conjunto__practica__isnull=False) \
            .filter(conjunto__practica__numero=conjunto_de_enunciados)
    else:
        encontrados = encontrados.filter(conjunto__parcial__isnull=False)
        es_recuperatorio = tipo_conjunto == 'recuperatorio'
        encontrados = encontrados.filter(conjunto__parcial__recuperatorio=es_recuperatorio) \
            .filter(conjunto__parcial__numero=conjunto_de_enunciados)

    enunciado_encontrado = encontrados[0]
    return render_enunciado(enunciado_encontrado)


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

    return render_enunciado(encontrado)


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
