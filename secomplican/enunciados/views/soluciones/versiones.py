from django.shortcuts import render, get_object_or_404

from enunciados.models import Solucion

def versiones_solucion(request, pk):
    solucion = get_object_or_404(Solucion, pk=pk)
    return render(
        request, 'enunciados/versiones_solucion.html', {'solucion': solucion})