from django.shortcuts import render, redirect, get_object_or_404

from enunciados.models import Solucion


def volver_a_version(objeto, pk):
    version = get_object_or_404(objeto.versiones, pk=pk)
    version.pk = None
    version.save()


def versiones_solucion(request, pk):
    solucion = get_object_or_404(Solucion, pk=pk)
    if request.method == 'POST':
        # Nos postearon una versión a la que volver.
        # La versión está en version_pk.
        pk = request.POST.get('version_pk')
        if pk:
            volver_a_version(solucion, pk)
            return redirect(solucion.enunciado)

    return render(
        request, 'enunciados/versiones_solucion.html', {'solucion': solucion})