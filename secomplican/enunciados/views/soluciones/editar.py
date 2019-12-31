from django.forms import ModelForm, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from enunciados.models import Solucion, VersionTexto
from enunciados.utils import enunciados_url_parser
from enunciados.views.breadcrumb import breadcrumb_editar_solucion


class VersionTextoSolucionForm(ModelForm):
    def __init__(self, solucion, *args, **kwargs):
        self.solucion = solucion
        super().__init__(*args, **kwargs)

    def clean_texto(self):
        texto_anterior = self.solucion.versiones.ultima().texto
        texto_nuevo = self.cleaned_data['texto']
        if texto_nuevo == texto_anterior:
            raise ValidationError(_('No se cambió el texto.'))
        return texto_nuevo

    def save(self):
        self.instance.solucion = self.solucion
        return super().save()

    class Meta:
        model = VersionTexto
        fields = ['texto']


def editar_solucion(request, pk_solucion, **kwargs):
    materia_carrera = kwargs['materia_carrera']
    solucion = get_object_or_404(Solucion, pk=pk_solucion)
    if request.method == 'POST':
        form = VersionTextoSolucionForm(solucion, request.POST)
        if form.is_valid():
            form.save()
            success_url = enunciados_url_parser.url_enunciado(
                materia_carrera, solucion.enunciado)
            return redirect(success_url)
    else:
        form = VersionTextoSolucionForm(
            solucion, initial={'texto': solucion.versiones.ultima().texto})

    contexto = {
        'materia_carrera': materia_carrera,
        'carrera': materia_carrera.carrera,
        'form': form,
        'solucion': solucion,
        'enunciado': solucion.enunciado,
        'breadcrumb': breadcrumb_editar_solucion(
            materia_carrera, solucion.enunciado),
        'texto_boton': _('Enviar'),
    }
    return render(request, 'enunciados/nueva_solucion.html', contexto)
