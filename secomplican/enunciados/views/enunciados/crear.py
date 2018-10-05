from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView

from enunciados.models import Materia, Enunciado
from enunciados.utils import conjuntos_url_parser, enunciados_url_parser
from .forms import EnunciadoConConjuntoForm, VersionTextoForm


def nuevo_enunciado(request, **kwargs):
    conjunto = conjuntos_url_parser.kwargs_a_conjunto(kwargs)
    if request.method == 'POST':
        enunciado_form = EnunciadoConConjuntoForm(conjunto, request.POST)
        version_texto_form = VersionTextoForm(request.POST)
        if enunciado_form.is_valid() and version_texto_form.is_valid():
            enunciado = enunciado_form.save()
            version_texto = version_texto_form.save(commit=False)
            version_texto.enunciado = enunciado
            version_texto.save()
            materia_carrera = kwargs['materia_carrera']
            success_url = enunciados_url_parser.url_enunciado(
                materia_carrera, enunciado)
            return redirect(success_url)
    else:
        enunciado_form = EnunciadoConConjuntoForm(conjunto)
        version_texto_form = VersionTextoForm()

    context = {
        'enunciado_form': enunciado_form,
        'version_texto_form': version_texto_form,
    }
    return render(request, 'enunciados/nuevo_enunciado.html', context)
