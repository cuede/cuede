from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView

from enunciados.models import Materia, Enunciado, Posteo
from enunciados.utils import conjuntos_url_parser, enunciados_url_parser
from .forms import EnunciadoConConjuntoForm, VersionTextoForm
from enunciados.views.breadcrumb import breadcrumb_crear_enunciado


def nuevo_enunciado(request, **kwargs):
    conjunto = conjuntos_url_parser.kwargs_a_conjunto(kwargs)
    materia_carrera = kwargs['materia_carrera']
    if request.method == 'POST':
        enunciado_form = EnunciadoConConjuntoForm(conjunto, request.POST)
        version_texto_form = VersionTextoForm(request.POST)
        if enunciado_form.is_valid() and version_texto_form.is_valid():
            enunciado = enunciado_form.save()
            version_texto = version_texto_form.save(commit=False)
            version_texto.posteo = enunciado
            version_texto.save()
            success_url = enunciados_url_parser.url_enunciado(
                materia_carrera, enunciado)
            return redirect(success_url)
    else:
        enunciado_form = EnunciadoConConjuntoForm(conjunto)
        version_texto_form = VersionTextoForm()

    context = {
        'carrera': materia_carrera.carrera,
        'materia_carrera': materia_carrera,
        'enunciado_form': enunciado_form,
        'version_texto_form': version_texto_form,
        'breadcrumb': breadcrumb_crear_enunciado(materia_carrera, conjunto),
    }
    return render(request, 'enunciados/nuevo_enunciado.html', context)
