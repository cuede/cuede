from django.shortcuts import render

from enunciados.models import Carrera

def index(request):
    computacion = Carrera.objects.get(slug='computacion')
    return render(request, 'index.html', {'carrera': computacion})
