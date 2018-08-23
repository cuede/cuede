from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from enunciados.models import Materia

from .forms import ConjuntoDeEnunciadosForm, EnunciadoForm, VersionTextoForm


def nuevo_enunciado(request, materia):
    # objeto_materia = get_object_or_404(Materia, slug=materia)
    if request.method == 'POST':
        conjunto_form = ConjuntoDeEnunciadosForm(request.POST)
        enunciado_form = EnunciadoForm(request.POST)
        version_texto_form = VersionTextoForm(request.POST)
        if conjunto_form.is_valid() and \
                enunciado_form.is_valid() and version_texto_form.is_valid():
            conjunto, creado = conjunto_form.save()
            enunciado = enunciado_form.save(commit=False)
            enunciado.conjunto = conjunto
            hubo_error = False
            if not creado:
                # Hace falta fijarse si el número del enunciado está bien.
                # Eso se puede hacer directamente llamando a full_clean().
                try:
                    enunciado.full_clean()
                except ValidationError as error:
                    enunciado_form.add_error(None, error)
                    hubo_error = True

            if not hubo_error:
                enunciado.save()
                version_texto = version_texto_form.save(commit=False)
                version_texto.enunciado = enunciado
                version_texto.save()
                return redirect(enunciado.get_absolute_url())
    else:
        conjunto_form = ConjuntoDeEnunciadosForm(initial=request.GET)
        enunciado_form = EnunciadoForm()
        version_texto_form = VersionTextoForm()

    context = {'conjunto_form': conjunto_form, 'enunciado_form': enunciado_form,
               'version_texto_form': version_texto_form}
    return render(request, 'enunciados/nuevo_enunciado.html', context)
