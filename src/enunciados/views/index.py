from django.shortcuts import redirect

from enunciados.models import Carrera

def index(request):
    computacion = Carrera.objects.get(slug='computacion')
    return redirect('materias', carrera=computacion)
