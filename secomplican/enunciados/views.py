from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Se complican :)")

def materias(resuest):    
    return HttpResponse("Ac'a va el listado de las materias.");
