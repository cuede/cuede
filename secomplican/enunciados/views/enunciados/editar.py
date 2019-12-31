from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from enunciados.utils import enunciados_url_parser

from .forms import EnunciadoConConjuntoForm, VersionTextoForm
from enunciados.views.breadcrumb import breadcrumb_editar_enunciado


def se_cambio_texto(enunciado, texto_nuevo):
    texto_anterior = enunciado.versiones.ultima().texto
    return texto_anterior != texto_nuevo


def enunciado(request, **kwargs):
    materia_carrera = kwargs['materia_carrera']
    enunciado_encontrado = enunciados_url_parser.kwargs_a_enunciado(kwargs)
    conjunto = enunciado_encontrado.conjunto
    if request.method == 'POST':
        numero_anterior = enunciado_encontrado.numero
        enunciado_form = EnunciadoConConjuntoForm(
            conjunto, request.POST, instance=enunciado_encontrado)
        version_texto_form = VersionTextoForm(request.POST)
        if enunciado_form.is_valid() and version_texto_form.is_valid():
            hubo_error = False

            nuevo_numero = enunciado_form.cleaned_data['numero']
            texto_nuevo = version_texto_form.cleaned_data['texto']
            cambio_texto = se_cambio_texto(enunciado_encontrado, texto_nuevo)
            if numero_anterior == nuevo_numero and not cambio_texto:
                version_texto_form.add_error(
                    'texto', ValidationError(_('No se cambió el texto.'))
                )
                hubo_error = True

            if not hubo_error:
                enunciado = enunciado_form.save()
                if cambio_texto:
                    version_texto = version_texto_form.save(commit=False)
                    version_texto.posteo = enunciado
                    version_texto.save()
                success_url = enunciados_url_parser.url_enunciado(
                    materia_carrera, enunciado)
                return redirect(success_url)
    else:
        enunciado_form = EnunciadoConConjuntoForm(
            conjunto,
            initial={'numero': enunciado_encontrado.numero}
        )
        version_texto_form = VersionTextoForm(
            initial={'texto': enunciado_encontrado.versiones.ultima().texto}
        )

    context = {
        'materia_carrera': materia_carrera,
        'carrera': materia_carrera.carrera,
        'enunciado_form': enunciado_form,
        'version_texto_form': version_texto_form,
        'breadcrumb': breadcrumb_editar_enunciado(
            materia_carrera, enunciado_encontrado)
    }
    return render(request, 'enunciados/editar_enunciado.html', context)
