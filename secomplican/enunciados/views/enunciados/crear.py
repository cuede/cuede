from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.db.models import F

from django.contrib.auth.decorators import login_required

from enunciados.models import Materia, Enunciado, Posteo
from enunciados.utils import conjuntos_url_parser, enunciados_url_parser
from .forms import EnunciadoConConjuntoForm, VersionTextoForm
from enunciados.views.breadcrumb import breadcrumb_crear_enunciado


PUNTOS_USUARIO_POR_CREAR_ENUNCIADO = 10


def render_nuevo_enunciado(
    request, materia_carrera, enunciado_form, version_texto_form, conjunto):
    context = {
        'carrera': materia_carrera.carrera,
        'materia_carrera': materia_carrera,
        'enunciado_form': enunciado_form,
        'version_texto_form': version_texto_form,
        'breadcrumb': breadcrumb_crear_enunciado(materia_carrera, conjunto),
    }
    return render(request, 'enunciados/nuevo_enunciado.html', context)


def crear_enunciado_con_forms(enunciado_form, version_texto_form, usuario_creador):
    enunciado = enunciado_form.save()
    version_texto = version_texto_form.save(commit=False)
    version_texto.posteo = enunciado
    version_texto.save()
    informacion_usuario = usuario_creador.informacionusuario
    informacion_usuario.puntos = F('puntos') + PUNTOS_USUARIO_POR_CREAR_ENUNCIADO
    informacion_usuario.save()
    return enunciado


def handle_post(request, materia_carrera, conjunto):
    enunciado_form = EnunciadoConConjuntoForm(conjunto, request.POST)
    version_texto_form = VersionTextoForm(request.POST)
    if enunciado_form.is_valid() and version_texto_form.is_valid():
        enunciado = crear_enunciado_con_forms(enunciado_form, version_texto_form, request.user)
        success_url = enunciados_url_parser.url_enunciado(
            materia_carrera, enunciado)
        response = redirect(success_url)
    else:
        response = render_nuevo_enunciado(
            request, materia_carrera, enunciado_form, version_texto_form, conjunto)

    return response


def handle_get(request, materia_carrera, conjunto):
    enunciado_form = EnunciadoConConjuntoForm(conjunto)
    version_texto_form = VersionTextoForm()

    return render_nuevo_enunciado(
        request, materia_carrera, enunciado_form, version_texto_form, conjunto)


@login_required
def nuevo_enunciado(request, **kwargs):
    conjunto = conjuntos_url_parser.kwargs_a_conjunto(kwargs)
    materia_carrera = kwargs['materia_carrera']
    if request.method == 'POST':
        response = handle_post(request, materia_carrera, conjunto)
    else:
        response = handle_get(request, materia_carrera, conjunto)
    return response
