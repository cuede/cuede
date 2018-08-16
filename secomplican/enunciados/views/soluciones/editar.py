from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from enunciados.models import Solucion

def editar_solucion(request, pk):
    solucion = get_object_or_404(Solucion, pk=pk)
    return HttpResponse(str(solucion))
