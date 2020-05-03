from django import forms
from django.shortcuts import render

from enunciados.utils import conjuntos_url_parser, enunciados_url_parser
from enunciados.views.breadcrumb import breadcrumb_conjunto_de_enunciados
from enunciados.views.conjuntos_de_enunciados.validators.extension_validator import \
    validate_extension
from enunciados.views.conjuntos_de_enunciados.validators.max_size_validator import validate_max_size
from enunciados.views.conjuntos_de_enunciados.validators.mime_type_validator import \
    validate_allowed_mime_type


class ArchivoDeConjuntoDeEnunciadosForm(forms.Form):
    archivo = forms.FileField(
        validators=[validate_max_size, validate_allowed_mime_type, validate_extension]
    )

    def __init__(self, data=None, files=None, conjunto=None, *args, **kwargs):
        super(ArchivoDeConjuntoDeEnunciadosForm, self).__init__(
            data=data, files=files, *args, **kwargs)
        self.conjunto = conjunto

    def save(self):
        archivo = self.cleaned_data['archivo']
        archivo_anterior = self.conjunto.archivo
        nombre_archivo_anterior = archivo_anterior.name
        self.conjunto.archivo = archivo
        self.conjunto.save()
        if nombre_archivo_anterior != self.conjunto.archivo.name:
            archivo_anterior.delete(save=False)


def conjunto_de_enunciados(request, **kwargs):
    materia_carrera = kwargs['materia_carrera']
    conjunto = conjuntos_url_parser.kwargs_a_conjunto(kwargs)
    url_nuevo_enunciado = enunciados_url_parser.url_nuevo_enunciado(materia_carrera, conjunto)
    if request.method == 'POST':
        form = ArchivoDeConjuntoDeEnunciadosForm(request.POST, request.FILES, conjunto)
        if form.is_valid():
            form.save()
            conjunto.refresh_from_db()
    else:
        form = ArchivoDeConjuntoDeEnunciadosForm()
    contexto = {
        'carrera': materia_carrera.carrera,
        'materia_carrera': materia_carrera,
        'conjunto': conjunto,
        'archivo_de_conjunto_de_enunciados_form': form,
        'url_nuevo_enunciado': url_nuevo_enunciado,
        'breadcrumb': breadcrumb_conjunto_de_enunciados(
            materia_carrera, conjunto),
    }
    return render(request, 'enunciados/conjunto/ver.html', contexto)
