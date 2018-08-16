from django.forms import ModelForm
from django.shortcuts import get_object_or_404, redirect, render

from enunciados.models import Solucion, VersionTextoSolucion


class VersionTextoSolucionForm(ModelForm):
    class Meta:
        model = VersionTextoSolucion
        fields = ['texto']


def editar_solucion(request, pk):
    solucion = get_object_or_404(Solucion, pk=pk)
    if request.method == 'POST':
        form = VersionTextoSolucionForm(request.POST)
        if form.is_valid():
            version_texto = form.save(commit=False)
            version_texto.solucion = solucion
            version_texto.save()
            return redirect(solucion.enunciado)
    else:
        form = VersionTextoSolucionForm(
            initial={'texto': solucion.versiones.ultima().texto})

    return render(request, 'enunciados/editar_solucion.html', {'form': form})
