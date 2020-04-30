from django.shortcuts import redirect, render

from enunciados.models import get_sentinel_user
from enunciados.utils import conjuntos_url_parser, enunciados_url_parser
from enunciados.views.breadcrumb import breadcrumb_crear_enunciado
from .forms import EnunciadoConConjuntoForm, VersionTextoForm

PUNTOS_USUARIO_POR_CREAR_ENUNCIADO = 10


def nuevo_enunciado(request, **kwargs):
    conjunto = conjuntos_url_parser.kwargs_a_conjunto(kwargs)
    materia_carrera = kwargs['materia_carrera']
    if request.method == 'POST':
        response = handle_post(request, materia_carrera, conjunto)
    else:
        response = handle_get(request, materia_carrera, conjunto)
    return response


def handle_post(request, materia_carrera, conjunto):
    enunciado_form = EnunciadoConConjuntoForm(conjunto, request.POST)
    version_texto_form = VersionTextoForm(request.POST)

    if puede_guardar_enunciado(enunciado_form, version_texto_form, conjunto):
        response = guardar_enunciado(enunciado_form, materia_carrera, version_texto_form)
    else:
        response = render_nuevo_enunciado(
            request, materia_carrera, enunciado_form, version_texto_form, conjunto)

    return response


def puede_guardar_enunciado(enunciado_form, version_texto_form, conjunto):
    return enunciado_form.is_valid() and (conjunto.archivo or version_texto_form.is_valid())


def guardar_enunciado(enunciado_form, materia_carrera, version_texto_form):
    enunciado = enunciado_form.save()
    success_url = enunciados_url_parser.url_enunciado(materia_carrera, enunciado)
    if version_texto_form.is_valid():
        guardar_version_texto(enunciado, version_texto_form, get_sentinel_user())
    response = redirect(success_url)
    return response


def guardar_version_texto(enunciado, version_texto_form, usuario_creador):
    version_texto = version_texto_form.save(commit=False)
    version_texto.posteo = enunciado
    version_texto.autor = usuario_creador
    version_texto.save()


def render_nuevo_enunciado(
        request, materia_carrera, enunciado_form, version_texto_form, conjunto):
    context = {
        'carrera': materia_carrera.carrera,
        'materia_carrera': materia_carrera,
        'enunciado_form': enunciado_form,
        'version_texto_form': version_texto_form,
        'breadcrumb': breadcrumb_crear_enunciado(materia_carrera, conjunto),
        'conjunto': conjunto,
    }
    return render(request, 'enunciados/nuevo_enunciado.html', context)


def handle_get(request, materia_carrera, conjunto):
    enunciado_form = EnunciadoConConjuntoForm(conjunto)
    version_texto_form = VersionTextoForm()

    return render_nuevo_enunciado(
        request, materia_carrera, enunciado_form, version_texto_form, conjunto)
