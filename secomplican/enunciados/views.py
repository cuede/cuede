from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Se complican :)")


def materias(request):
    return HttpResponse("Acá va el listado de las materias.")
