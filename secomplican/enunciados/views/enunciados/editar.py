from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.db.models import F

from enunciados.utils import enunciados_url_parser

from .forms import EnunciadoConConjuntoForm, VersionTextoForm
from enunciados.views.breadcrumb import breadcrumb_editar_enunciado


PUNTOS_USUARIO_EDITAR_ENUNCIADO = 5


def se_cambio_texto(enunciado, texto_nuevo):
    texto_anterior = enunciado.versiones.ultima().texto
    return texto_anterior != texto_nuevo


def sumar_puntos_por_edicion(usuario):
    informacion_usuario = usuario.informacionusuario
    informacion_usuario.puntos = F('puntos') + PUNTOS_USUARIO_EDITAR_ENUNCIADO
    informacion_usuario.save()


def render_editar_enunciado(
    request, materia_carrera, enunciado_form, version_texto_form, enunciado_encontrado):
    context = {
        'materia_carrera': materia_carrera,
        'carrera': materia_carrera.carrera,
        'enunciado_form': enunciado_form,
        'version_texto_form': version_texto_form,
        'breadcrumb': breadcrumb_editar_enunciado(
            materia_carrera, enunciado_encontrado)
    }
    return render(request, 'enunciados/editar_enunciado.html', context)


def no_edito_enunciado(enunciado, usuario):
    return enunciado.versiones.filter(autor=usuario).count() == 0


def crear_enunciado_con_forms(
    enunciado_form, version_texto_form, usuario_creador, cambio_texto):
    enunciado = enunciado_form.save()
    if cambio_texto:
        deberia_sumar_puntos = no_edito_enunciado(enunciado, usuario_creador)
        version_texto = version_texto_form.save(commit=False)
        version_texto.posteo = enunciado
        version_texto.autor = usuario_creador
        version_texto.save()
        if deberia_sumar_puntos:
            sumar_puntos_por_edicion(usuario_creador)
    return enunciado


def handle_post(request, materia_carrera, conjunto, enunciado_encontrado):
    numero_anterior = enunciado_encontrado.numero
    enunciado_form = EnunciadoConConjuntoForm(
        conjunto, request.POST, instance=enunciado_encontrado)
    version_texto_form = VersionTextoForm(request.POST)

    response = None
    if enunciado_form.is_valid() and version_texto_form.is_valid():
        nuevo_numero = enunciado_form.cleaned_data['numero']
        texto_nuevo = version_texto_form.cleaned_data['texto']
        cambio_texto = se_cambio_texto(enunciado_encontrado, texto_nuevo)
        if numero_anterior == nuevo_numero and not cambio_texto:
            version_texto_form.add_error(
                'texto', ValidationError(_('No se cambió el texto.')))
        else:
            enunciado = crear_enunciado_con_forms(
                enunciado_form, version_texto_form, request.user, cambio_texto)
            success_url = enunciados_url_parser.url_enunciado(
                materia_carrera, enunciado)
            response = redirect(success_url)

    if not response:
        response = render_editar_enunciado(
            request, materia_carrera, enunciado_form, version_texto_form, enunciado_encontrado)
    return response


def handle_get(request, materia_carrera, conjunto, enunciado_encontrado):
    enunciado_form = EnunciadoConConjuntoForm(
        conjunto,
        initial={'numero': enunciado_encontrado.numero}
    )
    version_texto_form = VersionTextoForm(
        initial={'texto': enunciado_encontrado.versiones.ultima().texto}
    )

    return render_editar_enunciado(
        request, materia_carrera, enunciado_form, version_texto_form, enunciado_encontrado)


@login_required
def enunciado(request, **kwargs):
    materia_carrera = kwargs['materia_carrera']
    enunciado_encontrado = enunciados_url_parser.kwargs_a_enunciado(kwargs)
    conjunto = enunciado_encontrado.conjunto
    if request.method == 'POST':
        response = handle_post(request, materia_carrera, conjunto, enunciado_encontrado)
    else:
        response = handle_get(request, materia_carrera, conjunto, enunciado_encontrado)

    return response
