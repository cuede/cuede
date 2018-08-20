from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from enunciados.models import VersionTextoEnunciado
from enunciados.utils import cuatrimestres_url_parser

from . import enunciados_utils
from .forms import EnunciadoForm, VersionTextoForm


def se_cambio_texto(enunciado, texto_nuevo):
    texto_anterior = self.enunciado.versiones.ultima().texto
    return texto_anterior != texto_nuevo


def enunciado(request, enunciado):
    if request.method == 'POST':
        enunciado_form = EnunciadoForm(request.POST)
        version_texto_form = VersionTextoForm(request.POST)
        if enunciado_form.is_valid() and version_texto_form.is_valid():
            numero_anterior = enunciado.numero
            enunciado.numero = enunciado_form.cleaned_data['numero']
            hubo_error = False
            try:
                enunciado.full_clean()
            except ValidationError as error:
                enunciado_form.add_error(None, error)
                hubo_error = True

            if enunciado.numero == numero_anterior:
                texto_nuevo = version_texto_form.cleaned_data['texto']
                if not se_cambio_texto(enunciado, texto_nuevo):
                    version_texto_form.add_error(
                        'texto', ValidationError(_('No se cambió el texto.'))
                    )
                    hubo_error = True

            if not hubo_error:
                enunciado.save()
                version_texto = version_texto_form.save(commit=False)
                version_texto.enunciado = enunciado
                version_texto.save()
                return redirect(enunciado.get_absolute_url())
    else:
        enunciado_form = EnunciadoForm(
            initial={'numero': enunciado.numero}
        )
        version_texto_form = VersionTextoForm(
            initial={'texto': enunciado.versiones.ultima().texto}
        )

    context = {
        'enunciado_form': enunciado_form,
        'version_texto_form': version_texto_form,
    }
    return render(request, 'enunciados/editar_enunciado.html', context)


def enunciado_practica(
        request, materia, anio, cuatrimestre, numero_practica, numero):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = enunciados_utils.enunciado_de_practica(
        materia, anio, numero_cuatrimestre, numero_practica, numero)
    return enunciado(request, encontrado)


def enunciado_parcial(
        request, materia, anio, cuatrimestre, numero_parcial,
        numero, es_recuperatorio):
    numero_cuatrimestre = cuatrimestres_url_parser.url_a_numero(cuatrimestre)
    encontrado = enunciados_utils.enunciado_de_parcial(
        materia, anio, numero_cuatrimestre, numero_parcial,
        numero, es_recuperatorio)
    return enunciado(request, encontrado)


def enunciado_final(request,  materia, anio, mes, dia, numero):
    encontrado = enunciados_utils.enunciado_de_final(
        materia, anio, mes, dia, numero)
    return enunciado(request, encontrado)
