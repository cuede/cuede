from django.forms import ModelForm, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from enunciados.models import Solucion, VersionTextoSolucion


class VersionTextoSolucionForm(ModelForm):
    def __init__(self, solucion, *args, **kwargs):
        self.solucion = solucion
        super().__init__(*args, **kwargs)

    def clean_texto(self):
        texto_anterior = self.solucion.versiones.ultima().texto
        texto_nuevo = self.cleaned_data['texto']
        if texto_nuevo == texto_anterior:
            raise ValidationError(_('No se cambió el texto.'))

    class Meta:
        model = VersionTextoSolucion
        fields = ['texto']


def editar_solucion(request, pk):
    solucion = get_object_or_404(Solucion, pk=pk)
    if request.method == 'POST':
        form = VersionTextoSolucionForm(solucion, request.POST)
        if form.is_valid():
            version_texto = form.save(commit=False)
            version_texto.solucion = solucion
            version_texto.save()
            return redirect(solucion.enunciado)
    else:
        form = VersionTextoSolucionForm(
            solucion, initial={'texto': solucion.versiones.ultima().texto})

    contexto = {
        'form': form,
        'solucion': solucion,
    }
    return render(request, 'enunciados/editar_solucion.html', contexto)
