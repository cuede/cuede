from django import forms
from django.shortcuts import render

from enunciados.utils import conjuntos_url_parser, enunciados_url_parser
from enunciados.views.breadcrumb import breadcrumb_conjunto_de_enunciados


class ArchivoDeConjuntoDeEnunciadosForm(forms.Form):
    archivo = forms.FileField()

    def __init__(self, data=None, files=None, conjunto=None, *args, **kwargs):
        super(ArchivoDeConjuntoDeEnunciadosForm, self).__init__(
            data=data, files=files, *args, **kwargs)
        self.conjunto = conjunto

    def save(self):
        archivo = self.cleaned_data['archivo']
        self.conjunto.archivo.delete()
        self.conjunto.archivo = archivo
        self.conjunto.save()


def conjunto_de_enunciados(request, **kwargs):
    materia_carrera = kwargs['materia_carrera']
    conjunto = conjuntos_url_parser.kwargs_a_conjunto(kwargs)
    url_nuevo_enunciado = enunciados_url_parser.url_nuevo_enunciado(materia_carrera, conjunto)
    if request.method == 'POST':
        form = ArchivoDeConjuntoDeEnunciadosForm(request.POST, request.FILES, conjunto)
        if form.is_valid():
            form.save()
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
    return render(request, 'enunciados/conjunto_de_enunciados.html', contexto)
