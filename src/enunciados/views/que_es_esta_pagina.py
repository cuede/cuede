from django.shortcuts import render
from enunciados.models import Carrera


def que_es_esta_pagina(request):
    computacion = Carrera.objects.get(slug='computacion')
    return render(request, 'que_es_esta_pagina.html', {'carrera': computacion})
